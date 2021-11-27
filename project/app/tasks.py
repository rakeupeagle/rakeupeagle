# Standard Libary
import csv

import geocoder
import requests
# First-Party
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
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
from twilio.rest import Client as TwilioClient

# Local
from .models import Assignment
from .models import Message
from .models import Picture
from .models import Recipient
from .models import Team


# Auth0
def get_auth0_token():
    get_token = GetToken(settings.AUTH0_DOMAIN)
    token = get_token.client_credentials(
        settings.AUTH0_CLIENT_ID,
        settings.AUTH0_CLIENT_SECRET,
        f'https://{settings.AUTH0_DOMAIN}/api/v2/',
    )
    return token

def get_auth0_client():
    token = get_auth0_token()
    client = Auth0(
        settings.AUTH0_DOMAIN,
        token['access_token'],
    )
    return client

def get_twilio_client():
    client = TwilioClient()
    return client


def get_user_data(user_id):
    client = get_auth0_client()
    data = client.users.get(user_id)
    return data

def put_auth0_payload(endpoint, payload):
    token = get_auth0_token()
    access_token = token['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.put(
        f'https://{settings.AUTH0_DOMAIN}/api/v2/{endpoint}',
        headers=headers,
        json=payload,
    )
    return response

@job
def update_user(user):
    data = get_user_data(user.username)
    user.data = data
    user.name = data.get('name', '')
    user.first_name = data.get('given_name', '')
    user.last_name = data.get('family_name', '')
    user.email = data.get('email', None)
    user.phone = data.get('phone_number', None)
    user.save()
    return user


# Utility
def build_email(template, subject, from_email, context=None, to=[], cc=[], bcc=[], attachments=[], html_content=None):
    body = render_to_string(template, context)
    if html_content:
        html_rendered = render_to_string(html_content, context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to,
        cc=cc,
        bcc=bcc,
    )
    if html_content:
        email.attach_alternative(html_rendered, "text/html")
    for attachment in attachments:
        with attachment[1].open() as f:
            email.attach(attachment[0], f.read(), attachment[2])
    return email

@job
def send_email(email):
    return email.send()


def get_assignments_csv():
    gs = Assignment.objects.all()
    with open('assignments.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Recipient',
            'Team',
        ])
        for g in gs:
            writer.writerow([
                g.recipient.phone,
                g.team.phone,
            ])


def import_assignments_csv():
    with open('assignments.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            recipient = Recipient.objects.get(
                phone=row[0],
            )
            team = Team.objects.get(
                phone=row[1],
            )
            Assignment.objects.create(
                recipient=recipient,
                team=team,
            )


def get_teams_csv():
    ts = Team.objects.all()
    with open('teams.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Team',
            'Name',
            'Phone',
            'Size',
            'Reference',
            'Actual',
            'Notes',
            'Admin Notes',
        ])
        for t in ts:
            writer.writerow([
                t.team,
                t.name,
                t.phone,
                t.size,
                t.reference,
                t.actual,
                t.notes,
                t.admin_notes,
            ])


def get_recipients_csv():
    rs = Recipient.objects.all()
    with open('recipients.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Name',
            'Phone',
            'Size',
            'Location',
            'Place',
            'Is Precise',
            'Point',
            'Geocode',
            'Is Dog',
            'Notes',
            'Admin Notes',
            'Bags',
            'Hours',
        ])
        for r in rs:
            writer.writerow([
                r.name,
                r.phone,
                r.size,
                r.location,
                r.place,
                r.is_precise,
                r.point,
                r.geocode,
                r.is_dog,
                r.notes,
                r.admin_notes,
                r.bags,
                r.hours,
            ])

def import_recipients_csv():
    with open('recipients.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            Recipient.objects.create(
                name = row[0],
                phone = row[1],
                size = row[2],
                location = row[3],
                place = row[4],
                is_precise = row[5],
                point = row[6],
                geocode = row[7],
                is_dog = bool(row[8]),
                notes = row[9],
                admin_notes = row[10],
                bags = 0,
                hours = 0,
            )



def import_teams_csv():
    with open('teams.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            Team.objects.create(
                nickname = row[0],
                name = row[1],
                phone = row[2],
                size = row[3],
                reference = row[4],
                actual = 0,
                notes = row[6],
                admin_notes = row[7],
            )




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
def delete_user(user_id):
    client = get_auth0_client()
    response = client.users.delete(user_id)
    return response



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
        str(message.user.phone),
        message.body,
    )
    message.state = message.STATE.sent
    message.sid = response.sid
    message.to = response.to
    message.body = response.body
    message.direction = message.DIRECTION.outbound
    message.save()
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
    result = geocoder.google(recipient.location)
    geocode = result.json
    is_precise = get_precision(geocode)
    if is_precise:
        recipient.is_precise = True
        recipient.point = Point(
            geocode['lng'],
            geocode['lat'],
        )
        recipient.place = geocode['place']
    else:
        geocode['status'] = 'IMPRECISE'
        recipient.is_precise = False
    recipient.geocode = geocode
    return recipient
