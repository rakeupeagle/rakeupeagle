import geocoder
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django_rq import job
from twilio.rest import Client as TwilioClient


# Client
def get_twilio_client():
    client = TwilioClient(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
    )
    return client


# Geocoding
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
        recipient.place_id = geocode['place']
        recipient.location = geocode['address']
        recipient.save()
    return


# Messaging
def create_instance_message(instance, message):
    body = render_to_string(
        f'app/texts/{message}.txt',
        context={
            'instance': instance,
        },
    )
    message = instance.messages.create(
        to_phone=instance.phone,
        from_phone=settings.TWILIO_NUMBER,
        direction=20, #TODO Fix Hardcode
        body=body,
    )
    return message


def send_message(message):
    if message.sid:
        raise ValidationError("Message already has SID")

    if message.to_phone == settings.TWILIO_NUMBER:
        raise ValidationError("Can't send to Twilio Number")

    if message.direction != message.DirectionChoices.OUTBOUND:
        raise ValidationError("Message is not Outbound")

    # This is more than a little hacky....
    phone = getattr(
        message.user,
        'phone',
        getattr(
            message.recipient,
            'phone',
            getattr(
                message.team,
                'phone',
                None,
            )
        )
    )
    if not phone:
        raise ValidationError("Message target empty")

    client = get_twilio_client()
    response = client.messages.create(
        messaging_service_sid=settings.TWILIO_MESSAGING_SERVICE_SID,
        to=phone.as_e164,
        body=message.body,
    )
    return response
