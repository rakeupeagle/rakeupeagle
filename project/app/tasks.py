# Standard Libary
import csv
import logging

import geocoder
import requests
# First-Party
from dateutil import parser
# Django
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.http import FileResponse
from django.template.loader import render_to_string
from django_rq import job
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client as TwilioClient

# Local
from .models import Assignment
from .models import Message
from .models import Picture
from .models import Recipient
from .models import Team
from .models import User


def send(number):
    client = TwilioClient()
    client.verify.services(
        settings.TWILIO_VERIFY_SID,
    ).verifications.create(
        to=number,
        channel='sms',
    )

def check(number, code):
    client = TwilioClient()
    try:
        result = client.verify.services(
            settings.TWILIO_VERIFY_SID,
        ).verification_checks.create(
            to=number,
            code=code,
        )
    except TwilioRestException as e:
        # log.error(e)
        return False
    return result.status == 'approved'


# Utility
def export_teams_csv():
    ts = Team.objects.all()
    with open('teams.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Name',
            'Phone',
            'State',
            'Size',
            'Nickname',
            'Reference',
            'Notes',
            'Admin Notes',
        ])
        for t in ts:
            writer.writerow([
                t.name,
                t.phone,
                t.state,
                t.size,
                t.nickname,
                t.reference,
                t.notes,
                t.admin_notes,
            ])


def import_teams_csv():
    with open('teams.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            try:
                user = User.objects.get(
                    phone=row[1],
                )
            except User.DoesNotExist:
                user = None
            Team.objects.create(
                name = row[0],
                phone = row[1],
                state = row[2],
                size = row[3],
                nickname = row[4],
                reference = row[5],
                notes = row[6],
                admin_notes = row[7],
                user=user,
            )


def export_recipients_csv():
    rs = Recipient.objects.all()
    with open('recipients.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Name',
            'Phone',
            'State',
            'Size',
            'Location',
            'Place',
            'Is Precise',
            # 'Point',
            'Geocode',
            'Is Dog',
            'Notes',
            'Admin Notes',
        ])
        for r in rs:
            writer.writerow([
                r.name,
                r.phone,
                r.state,
                r.size,
                r.location,
                r.place,
                r.is_precise,
                # r.point,
                r.geocode,
                r.is_dog,
                r.notes,
                r.admin_notes,
            ])

def import_recipients_csv():
    with open('recipients.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            try:
                user = User.objects.get(
                    phone=row[1],
                )
            except User.DoesNotExist:
                user = None
            Recipient.objects.create(
                name = row[0],
                phone = row[1],
                state = row[2],
                size = row[3],
                location = row[4],
                place = row[5],
                is_precise = bool(row[6]),
                geocode = row[7],
                is_dog = bool(row[8]),
                notes = row[9],
                admin_notes = row[10],
                user=user,
            )

def export_assignments_csv():
    gs = Assignment.objects.all()
    with open('assignments.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Recipient',
            'Team',
        ])
        for g in gs:
            writer.writerow([
                g.recipient.name,
                g.team.name,
            ])


def import_assignments_csv():
    with open('assignments.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            recipient = Recipient.objects.get(
                name=row[0],
            )
            team = Team.objects.get(
                name=row[1],
            )
            Assignment.objects.create(
                recipient=recipient,
                team=team,
            )


def import_messages_csv():
    with open('messages.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            status = row[3]
            if status == 'delivered':
                direction = Message.DIRECTION.outbound
                phone = row[1]
            elif status == 'received':
                direction = Message.DIRECTION.inbound
                phone = row[0]
            else:
                raise Exception
            if phone == '14157132126':
                continue
            try:
                user = User.objects.get(
                    phone=phone,
                )
            except User.DoesNotExist:
                user = None
            created = parser.parse(row[4])
            Message.objects.create(
                to_phone=row[1],
                from_phone=row[0],
                sid=row[9],
                body=row[2],
                direction=direction,
                created=created,
                user=user,
            )



def import_r_calls_csv():
    with open('r.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            name = row[0]
            notes = row[5]
            try:
                recipient = Recipient.objects.get(
                    name=name,
                )
            except Recipient.DoesNotExist:
                print(row[0])
            recipient.admin_notes = notes
            recipient.save()


def import_t_calls_csv():
    with open('t.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            name = row[0]
            notes = row[4]
            try:
                team = Team.objects.get(
                    name=name,
                )
            except Team.DoesNotExist:
                print(row[0])
            team.admin_notes = notes
            team.save()


def get_messages_csv():
    ms = Message.objects.all()
    with open('messages.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'SID',
            'To Phone',
            'From Phone',
            'Body',
            'Direction',
            'Raw',
            'Created',
        ])
        for m in ms:
            writer.writerow([
                m.sid,
                m.to_phone,
                m.from_phone,
                m.body,
                m.direction,
                m.raw,
                m.created,
            ])

@job
def send_recipient_confirmation(recipient):
    body = render_to_string(
        'app/texts/recipient_confirmation.txt',
        context={
            'recipient': recipient,
        },
    )
    admin = User.objects.get(is_admin=True)
    message = Message.objects.create(
        user=admin,
        direction=Message.DIRECTION.outbound,
        body=body,
    )
    message = Message.objects.create(
        user=recipient.user,
        direction=Message.DIRECTION.outbound,
        body=body,
    )
    return message

@job
def send_team_confirmation(team):
    body = render_to_string(
        'app/texts/team_confirmation.txt',
        context={
            'team': team,
        },
    )
    admin = User.objects.get(is_admin=True)
    message = Message.objects.create(
        user=admin,
        direction=Message.DIRECTION.outbound,
        body=body,
    )
    message = Message.objects.create(
        user=team.user,
        direction=Message.DIRECTION.outbound,
        body=body,
    )
    return message

@job
def send_recipient_deadline(recipient):
    body = render_to_string(
        'app/texts/recipient_deadline.txt',
        context={
            'recipient': recipient,
        },
    )
    message = Message.objects.create(
        user=recipient.user,
        direction=Message.DIRECTION.outbound,
        body=body,
    )
    return message

@job
def send_team_checkin(team):
    body = render_to_string(
        'app/texts/team_checkin.txt',
        context={
            'team': team,
        },
    )
    message = Message.objects.create(
        user=team.user,
        direction=Message.DIRECTION.outbound,
        body=body,
    )
    return message

@job
def send_team_complete(team):
    body = render_to_string(
        'app/texts/team_complete.txt',
        context={
            'team': team,
        },
    )
    message = Message.objects.create(
        user=team.user,
        direction=Message.DIRECTION.outbound,
        body=body,
    )
    return message

@job
def send_team_deadline(team):
    body = render_to_string(
        'app/texts/team_deadline.txt',
        context={
            'team': team,
        },
    )
    message = Message.objects.create(
        user=team.user,
        direction=Message.DIRECTION.outbound,
        body=body,
    )
    return message

@job
def create_and_upload_picture(path):
    with open(path, 'rb') as f:
        imagefile = File(f)
        picture = Picture.objects.create()
        picture.image.save('null', imagefile)


@job
def send_text(to, body, media_url=None):
    client = TwilioClient()
    if media_url:
        response = client.messages.create(
            to=to,
            from_=settings.TWILIO_NUMBER,
            body=body,
            media_url=media_url,
        )
        return response
    response = client.messages.create(
        to=to,
        from_=settings.TWILIO_NUMBER,
        body=body,
    )
    return response

@job
def send_text_from_message(message):
    if message.direction != message.DIRECTION.outbound:
        return
    response = send_text(
        message.to_phone.as_e164,
        message.body,
    )
    message.state = message.STATE.sent
    message.sid = response.sid
    message.to_phone = response.to
    # message.from_phone = response.from
    message.body = response.body
    message.direction = message.DIRECTION.outbound
    message.save()
    return


@job
def send_copy_from_message(message):
    if message.direction != message.DIRECTION.inbound:
        return
    admin = User.objects.get(is_admin=True)
    response = send_text(
        str(admin.phone),
        message.body,
    )
    return


@job
def send_team_final(team):
    body = render_to_string(
        'app/texts/team_final.txt',
        {'team': team},
    )
    response = send_text(
        str(team.phone),
        body,
    )
    return response

@job
def send_team_extra(team):
    body = render_to_string(
        'app/texts/team_extra.txt',
        {'team': team},
    )
    response = send_text(
        str(team.phone),
        body,
    )
    return response

@job
def send_team_rain(team):
    body = render_to_string(
        'app/texts/team_rain.txt',
        {'team': team},
    )
    response = send_text(
        str(team.phone),
        body,
    )
    return response

@job
def send_team_assignment(assignment):
    body = render_to_string(
        'app/texts/team_assignment.txt',
        {'assignment': assignment},
    )
    response = send_text(
        str(assignment.team.phone),
        body,
    )
    return response

@job
def send_recipient_rain(recipient):
    body = render_to_string(
        'app/texts/recipient_rain.txt',
        {'recipient': recipient},
    )
    response = send_text(
        str(recipient.phone),
        body,
    )
    return response

@job
def send_recipient_final(recipient):
    body = render_to_string(
        'app/texts/recipient_final.txt',
        {'recipient': recipient},
    )
    response = send_text(
        str(recipient.phone),
        body,
    )
    return response


@job
def send_recipient_checkin(recipient):
    body = render_to_string(
        'app/texts/recipient_checkin.txt',
        {'recipient': recipient},
    )
    response = send_text(
        str(recipient.phone),
        body,
    )
    return response


@job
def send_fix(phone):
    body = render_to_string(
        'app/texts/fix.txt',
    )
    response = send_text(
        str(phone),
        body,
    )
    return response


@job
def send_recipient_close(recipient):
    body = render_to_string(
        'app/texts/recipient_close.txt',
        {'recipient': recipient},
    )
    response = send_text(
        str(recipient.phone),
        body,
    )
    return response


@job
def send_assignment_pairs(recipient):
    assignments = recipient.assignments.all()
    for assignment in assignments:
        body = render_to_string(
            'app/texts/team_pair.txt',
            {
                'recipient': assignment.recipient,
                'assignments': assignments,
            },
        )
        response = send_text(
            str(assignment.team.phone),
            body,
        )
        return response


@job
def send_team_survey(team):
    body = render_to_string(
        'app/texts/team_survey.txt',
        {'team': team},
    )
    response = send_text(
        str(team.phone),
        body,
    )
    return response


def assign_team_from_recipient(recipient):
    team = Team.objects.filter(
        assignments__isnull=True,
    ).order_by(
        'size',
    ).last()
    if not team:
        raise Team.DoesNotExist
    recipient.assignments.create(
        team=team,
    )
    return recipient


def get_precision(geocode):
    return all([
        geocode['accuracy'] == 'ROOFTOP',
        any([
            geocode['quality'] == 'premise',
            geocode['quality'] == 'subpremise',
            geocode['quality'] == 'street_address',
        ])
    ])


@job
def geocode_recipient(recipient):
    address = f"{recipient.location}, Eagle ID  83616"
    result = geocoder.google(address)
    geocode = result.json
    try:
        is_precise = get_precision(geocode)
    except TypeError:
        return
    if is_precise:
        recipient.is_precise = True
        # recipient.point = Point(
        #     geocode['lng'],
        #     geocode['lat'],
        # )
        recipient.place = geocode['place']
    else:
        geocode['status'] = 'IMPRECISE'
        recipient.is_precise = False
    recipient.geocode = geocode
    return recipient.save()


def create_or_update(message):
    if message.direction.startswith("outbound"):
        phone = message.to
        direction = Message.DIRECTION.outbound
    elif message.direction.startswith('inbound'):
        phone = message.from_
        direction = Message.DIRECTION.inbound
    else:
        raise Exception('direction')
    user = User.objects.get(phone=phone)
    if user.is_admin:
        return None, None
    defaults = {
        'to_phone': message.to,
        'from_phone': message.from_,
        'body': message.body,
        'direction': direction,
        'user': user,
    }
    message, created = Message.objects.update_or_create(
        sid=message.sid,
        defaults=defaults,
    )
    return message, created
