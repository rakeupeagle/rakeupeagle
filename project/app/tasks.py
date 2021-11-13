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
from .models import Account
from .models import Assignment
from .models import Message
from .models import Picture
from .models import Recipient
from .models import Volunteer


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


def create_account_from_user(user):
    account = Account.objects.create(
        name=user.name,
        email=user.email,
        phone=user.phone,
        user=user,
    )
    return account

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
    gs = Assignment.objects.order_by(
        'volunteer__name',
    )
    with open('export.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Team Leader',
            'Team Phone',
            'Team Size',
            'Recipient Name',
            'Recipient Phone',
            'Recipient Size',
            'Recipient Location',
        ])
        for g in gs:
            writer.writerow([
                g.volunteer.name,
                g.volunteer.phone.as_national,
                g.volunteer.get_size_display(),
                g.recipient.name,
                g.recipient.phone.as_national,
                g.recipient.get_size_display(),
                g.recipient.location,
            ])
        return ContentFile(f)


@job
def send_recipient_confirmation(recipient):
    body = render_to_string(
        'app/texts/recipient_confirmation.txt',
        context={
            'recipient': recipient,
        },
    )
    message = Message.objects.create(
        account=recipient.account,
        direction=Message.DIRECTION.outbound,
        body=body,
    )
    return message

@job
def send_volunteer_confirmation(volunteer):
    body = render_to_string(
        'app/texts/volunteer_confirmation.txt',
        context={
            'volunteer': volunteer,
        },
    )
    message = Message.objects.create(
        account=volunteer.account,
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
        str(message.account.user.phone),
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
def send_volunteer_final(volunteer):
    body = render_to_string(
        'app/texts/volunteer_final.txt',
        {'volunteer': volunteer},
    )
    response = send_text(
        str(volunteer.phone),
        body,
    )
    return response

@job
def send_volunteer_extra(volunteer):
    body = render_to_string(
        'app/texts/volunteer_extra.txt',
        {'volunteer': volunteer},
    )
    response = send_text(
        str(volunteer.phone),
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
def send_volunteer_survey(volunteer):
    body = render_to_string(
        'app/texts/volunteer_survey.txt',
        {'volunteer': volunteer},
    )
    response = send_text(
        str(volunteer.phone),
        body,
    )
    return response


def assign_volunteer_from_recipient(recipient):
    volunteer = Volunteer.objects.filter(
        assignments__isnull=True,
    ).order_by(
        'size',
    ).last()
    if not volunteer:
        raise Volunteer.DoesNotExist
    recipient.assignments.create(
        volunteer=volunteer,
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
