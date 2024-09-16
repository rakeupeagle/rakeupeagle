import logging

from django.conf import settings
from django_rq import job
from twilio.rest import Client as TwilioClient

from .models import Event
from .models import Message
from .models import Recipient
from .models import Team
from .models import User

log = logging.getLogger(__name__)


# Twilio
def get_twilio_client():
    client = TwilioClient(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
    )
    return client



@job('default')
def create_message(message):
    client = get_twilio_client()
    if message.direction == Message.DirectionChoices.INBOUND or message.sid:
        return
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
    is_empty = all([
        not(message.recipient),
        not(message.team),
        not(message.user),
    ])
    if is_empty:
        log.error("Message target empty")
        return
    is_unclear = all([
        message.recipient,
        message.team,
    ])
    if is_unclear:
        log.error("Message target unclear")
        return
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
    response = client.messages.create(
        messaging_service_sid=settings.TWILIO_MESSAGING_SERVICE_SID,
        to=phone.as_e164,
        body=message.body,
    )
    message.sid = response.sid
    message.direction = Message.DirectionChoices.OUTBOUND
    return response


@job('default')
def delete_message(message):
    return


def process_webhook(data):
    message, _ = Message.objects.get_or_create(
        sid=data['MessageSid'],
    )
    try:
        recipient = Recipient.objects.get(
            phone=data['From'],
            event__state=Event.StateChoices.CURRENT,
        )
    except Recipient.DoesNotExist:
        recipient = None
    try:
        team = Team.objects.get(
            phone=data['From'],
            event__state=Event.StateChoices.CURRENT,
        )
    except Team.DoesNotExist:
        team = None
    try:
        user = User.objects.get(
            phone=data['From'],
        )
    except User.DoesNotExist:
        user = None
    message.state = message.StateChoices.NEW
    message.direction = message.DirectionChoices.INBOUND
    message.to_phone = settings.TWILIO_NUMBER
    message.from_phone = data['From']
    message.body = data['Body']
    message.raw = data
    message.recipient = recipient
    message.team = team
    message.user = user
    message.save()
    return
