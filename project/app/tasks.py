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


@job
def send_recipient_confirmation(recipient):
    body = render_to_string(
        'app/texts/recipient_confirmation.txt',
        context={
            'recipient': recipient,
        },
    )
    message = recipient.messages.create(
        body=body,
    )
    return message

@job
def send_recipient_invitation(recipient):
    body = render_to_string(
        'app/texts/recipient_invitation.txt',
        context={
            'recipient': recipient,
        },
    )
    message = recipient.messages.create(
        body=body,
        is_read=True,
    )
    # recipient.state = Recipient.StateChoices.INVITED
    # recipient.save()
    return message

@job
def send_recipient_accepted(recipient):
    body = render_to_string(
        'app/texts/recipient_accepted.txt',
        context={
            'recipient': recipient,
        },
    )
    message = recipient.messages.create(
        body=body,
        is_read=True,
    )
    return message

@job
def send_recipient_declined(recipient):
    body = render_to_string(
        'app/texts/recipient_declined.txt',
        context={
            'recipient': recipient,
        },
    )
    message = recipient.messages.create(
        body=body,
        is_read=True,
    )
    # recipient.state = Recipient.StateChoices.DECLINED
    # recipient.save()
    return message

@job
def send_team_confirmation(team):
    body = render_to_string(
        'app/texts/team_confirmation.txt',
        context={
            'team': team,
        },
    )
    message = team.messages.create(
        body=body,
    )
    return message

# @job
# def send_recipient_deadline(recipient):
#     body = render_to_string(
#         'app/texts/recipient_deadline.txt',
#         context={
#             'recipient': recipient,
#         },
#     )
#     message = Message.objects.create(
#         user=recipient.user,
#         direction=Message.DIRECTION.outbound,
#         body=body,
#     )
#     return message

# @job
# def send_team_checkin(team):
#     body = render_to_string(
#         'app/texts/team_checkin.txt',
#         context={
#             'team': team,
#         },
#     )
#     message = Message.objects.create(
#         user=team.user,
#         direction=Message.DIRECTION.outbound,
#         body=body,
#     )
#     return message

# @job
# def send_team_complete(team):
#     body = render_to_string(
#         'app/texts/team_complete.txt',
#         context={
#             'team': team,
#         },
#     )
#     message = Message.objects.create(
#         user=team.user,
#         direction=Message.DIRECTION.outbound,
#         body=body,
#     )
#     return message

# @job
# def send_team_deadline(team):
#     body = render_to_string(
#         'app/texts/team_deadline.txt',
#         context={
#             'team': team,
#         },
#     )
#     message = Message.objects.create(
#         user=team.user,
#         direction=Message.DIRECTION.outbound,
#         body=body,
#     )
#     return message

# @job
# def send_text(to, body, media_url=None):
#     client = TwilioClient()
#     if media_url:
#         response = client.messages.create(
#             to=to,
#             from_=settings.TWILIO_NUMBER,
#             body=body,
#             media_url=media_url,
#         )
#         return response
#     response = client.messages.create(
#         to=to,
#         from_=settings.TWILIO_NUMBER,
#         body=body,
#     )
#     return response

# @job
# def send_text_from_message(message):
#     if message.direction != message.DIRECTION.outbound:
#         return
#     response = send_text(
#         message.to_phone.as_e164,
#         message.body,
#     )
#     message.state = message.STATE.sent
#     message.sid = response.sid
#     message.to_phone = response.to
#     # message.from_phone = response.from
#     message.body = response.body
#     message.direction = message.DIRECTION.outbound
#     message.save()
#     return


# @job
# def send_copy_from_message(message):
#     if message.direction != message.DIRECTION.inbound:
#         return
#     admin = User.objects.get(is_admin=True)
#     response = send_text(
#         str(admin.phone),
#         message.body,
#     )
#     return


# @job
# def send_team_final(team):
#     body = render_to_string(
#         'app/texts/team_final.txt',
#         {'team': team},
#     )
#     response = send_text(
#         str(team.phone),
#         body,
#     )
#     return response

# @job
# def send_team_extra(team):
#     body = render_to_string(
#         'app/texts/team_extra.txt',
#         {'team': team},
#     )
#     response = send_text(
#         str(team.phone),
#         body,
#     )
#     return response

# @job
# def send_team_rain(team):
#     body = render_to_string(
#         'app/texts/team_rain.txt',
#         {'team': team},
#     )
#     response = send_text(
#         str(team.phone),
#         body,
#     )
#     return response

# @job
# def send_team_assignment(assignment):
#     body = render_to_string(
#         'app/texts/team_assignment.txt',
#         {'assignment': assignment},
#     )
#     response = send_text(
#         str(assignment.team.phone),
#         body,
#     )
#     return response

# @job
# def send_recipient_rain(recipient):
#     body = render_to_string(
#         'app/texts/recipient_rain.txt',
#         {'recipient': recipient},
#     )
#     response = send_text(
#         str(recipient.phone),
#         body,
#     )
#     return response

# @job
# def send_recipient_final(recipient):
#     body = render_to_string(
#         'app/texts/recipient_final.txt',
#         {'recipient': recipient},
#     )
#     response = send_text(
#         str(recipient.phone),
#         body,
#     )
#     return response


# @job
# def send_recipient_checkin(recipient):
#     body = render_to_string(
#         'app/texts/recipient_checkin.txt',
#         {'recipient': recipient},
#     )
#     response = send_text(
#         str(recipient.phone),
#         body,
#     )
#     return response


# @job
# def send_fix(phone):
#     body = render_to_string(
#         'app/texts/fix.txt',
#     )
#     response = send_text(
#         str(phone),
#         body,
#     )
#     return response


# @job
# def send_recipient_close(recipient):
#     body = render_to_string(
#         'app/texts/recipient_close.txt',
#         {'recipient': recipient},
#     )
#     response = send_text(
#         str(recipient.phone),
#         body,
#     )
#     return response


# @job
# def send_assignment_pairs(recipient):
#     assignments = recipient.assignments.all()
#     for assignment in assignments:
#         body = render_to_string(
#             'app/texts/team_pair.txt',
#             {
#                 'recipient': assignment.recipient,
#                 'assignments': assignments,
#             },
#         )
#         response = send_text(
#             str(assignment.team.phone),
#             body,
#         )
#         return response


# @job
# def send_team_survey(team):
#     body = render_to_string(
#         'app/texts/team_survey.txt',
#         {'team': team},
#     )
#     response = send_text(
#         str(team.phone),
#         body,
#     )
#     return response


# def assign_team_from_recipient(recipient):
#     team = Team.objects.filter(
#         assignments__isnull=True,
#     ).order_by(
#         'size',
#     ).last()
#     if not team:
#         raise Team.DoesNotExist
#     recipient.assignments.create(
#         team=team,
#     )
#     return recipient


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
    address = f"{recipient.location}, Eagle, ID"
    result = geocoder.google(address)
    geocode = result.json
    try:
        is_precise = get_precision(geocode)
    except TypeError:
        return
    if is_precise:
        recipient.point = Point(
            geocode['lng'],
            geocode['lat'],
        )
        recipient.save()
    return


# def create_or_update(message):
#     if message.direction.startswith("outbound"):
#         phone = message.to
#         direction = Message.DIRECTION.outbound
#     elif message.direction.startswith('inbound'):
#         phone = message.from_
#         direction = Message.DIRECTION.inbound
#     else:
#         raise Exception('direction')
#     user = User.objects.get(phone=phone)
#     if user.is_admin:
#         return None, None
#     defaults = {
#         'to_phone': message.to,
#         'from_phone': message.from_,
#         'body': message.body,
#         'direction': direction,
#         'user': user,
#     }
#     message, created = Message.objects.update_or_create(
#         sid=message.sid,
#         defaults=defaults,
#     )
#     return message, created
