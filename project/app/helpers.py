import logging
import re

from django.conf import settings
from twilio.rest import Client as TwilioClient

from .choices import DirectionChoices
from .choices import EventStateChoices
from .choices import MessageStateChoices
from .choices import RecipientStateChoices
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
                EventStateChoices.CURRENT,
                EventStateChoices.CLOSED,
            ],
        )
    except Recipient.DoesNotExist:
        recipient = None
    try:
        team = Team.objects.get(
            phone=data['From'],
            event__state__in=[
                EventStateChoices.CURRENT,
                EventStateChoices.CLOSED,
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
    message.state = MessageStateChoices.NEW
    message.direction = DirectionChoices.INBOUND
    message.to_phone = settings.TWILIO_NUMBER
    message.from_phone = data['From']
    message.body = data['Body']
    message.recipient = recipient
    message.team = team
    message.user = user
    message.save()

    # Probably should refactor this
    pattern = r'(?<=\[).{8}(?=\])'
    match = re.search(pattern, data['Body'])
    if not match:
        return
    assignee_id = match[0]
    try:
        assignee = Recipient.objects.get(
            id=assignee_id
        )
    except Recipient.DoesNotExist:
        assignee = None
    if assignee and team:
        if assignee.state == RecipientStateChoices.CONFIRMED:
            assignee.assigned = team
            assignee.save()
            assignee.assign()
            team.assign()
            team.save()
            assignee.save()
        elif assignee.state == RecipientStateChoices.ASSIGNED:
            team.complete()
            team.save()
            assignee.complete()
            assignee.save()
        else:
            log.error('state error')
    return
