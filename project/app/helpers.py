import logging

from django.conf import settings
from twilio.rest import Client as TwilioClient

from .models import Event
from .models import Message
from .models import Recipient
from .models import Team
from .models import User

log = logging.getLogger(__name__)


# Client
def get_twilio_client():
    client = TwilioClient(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
    )
    return client


# Verify
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
    result = client.verify.services(
        settings.TWILIO_VERIFY_SID,
    ).verification_checks.create(
        to=number,
        code=code,
    )
    return result.status == 'approved'


# Messaging
def inbound_message(data):
    message, _ = Message.objects.get_or_create(
        sid=data['MessageSid'],
    )
    try:
        recipient = Recipient.objects.get(
            phone=data['From'],
            event__state__in=[
                Event.StateChoices.CURRENT,
                Event.StateChoices.CLOSED,
            ],
        )
    except Recipient.DoesNotExist:
        recipient = None
    try:
        team = Team.objects.get(
            phone=data['From'],
            event__state__in=[
                Event.StateChoices.CURRENT,
                Event.StateChoices.CLOSED,
            ],
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
    message.recipient = recipient
    message.team = team
    message.user = user
    message.save()
    return
