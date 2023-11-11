import logging

from django.conf import settings
from django_rq import job
from twilio.rest import Client as TwilioClient

from .models import Content
from .models import Conversation
from .models import Message
from .models import Participant
from .models import Receipt

log = logging.getLogger(__name__)


# Twilio
def get_twilio_client():
    client = TwilioClient(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
    )
    return client

@job('default')
def create_conversation(conversation):
    if conversation.sid:
        return
    client = get_twilio_client()
    result = client.conversations.v1.conversations.create(
        friendly_name=conversation.name,
    )
    conversation.sid = result.sid
    conversation.date_created = result.date_created
    return


# @job('default')
# def update_conversation(conversation):
#     client = get_twilio_client()
#     client.conversations.v1.conversations(
#         conversation.conversation_sid
#     ).update(
#         name=conversation.name,
#         state=conversation.get_state_display(),
#         date_updated=conversation.date_updated,
#     )

@job('default')
def delete_conversation(conversation):
    client = get_twilio_client()
    client.conversations.v1.conversations(
        conversation.sid
    ).delete()
    return

@job('default')
def create_participant(participant):
    if participant.sid:
        return
    client = get_twilio_client()
    result = client.conversations.v1.conversations(
        participant.conversation.sid
    ).participants.create(
        messaging_binding_address=participant.phone.as_e164,
        messaging_binding_proxy_address=settings.TWILIO_NUMBER,
    )
    participant.sid = result.sid
    participant.date_created = result.date_created
    return

@job('default')
def delete_participant(participant):
    client = get_twilio_client()
    client.conversations.v1.conversations(
        participant.conversation.sid
    ).participants(
        participant.sid
    ).delete()
    return


@job('default')
def create_message(message):
    if message.sid:
        return
    client = get_twilio_client()
    if message.content:
        result = client.conversations.v1.conversations(
            message.conversation.sid
        ).messages.create(
            content_sid=message.content.sid,
        )
    else:
        result = client.conversations.v1.conversations(
            message.conversation.sid
        ).messages.create(
            body=message.body,
        )
    message.sid = result.sid
    message.date_created = result.date_created
    return

@job('default')
def delete_message(message):
    client = get_twilio_client()
    client.conversations.v1.conversations(
        message.conversation.sid
    ).messages(
        message.sid
    ).delete()
    return


# @job('default')
# def get_content(content_sid):
#     client = get_twilio_client()
#     result = client.content.v1.contents(
#         content_sid
#     ).fetch()
#     return result


# @job('default')
# def save_content(content_sid):
#     result = get_content(content_sid)
#     defaults = {
#         'name': result.name,
#         'components': result.types,
#         'variables': result.variables,
#     }
#     content, _ = Content.objects.update_or_create(
#         content_sid=content_sid,
#         defaults=defaults,
#     )
#     return content


def process_webhook(data):
    log.info(data)
    event_type = data['EventType']
    match event_type:
        # case 'onConversationStateUpdated':
        #     Conversation.objects.filter(
        #         sid=data['ConversationSid'],
        #     ).update(
        #         state=getattr(Conversation.STATE, data['StateTo']),
        #     )
        # case 'onParticipantAdded':
        #     Participant.objects.create(
        #         sid=data['ParticipantSid'],
        #         conversation_sid=data['ConversationSid'],
        #         phone=data['MessagingBinding.Address'],
        #         date_created=data['DateCreated'],
        #     )
        case 'onMessageAdded':
            sid = data.get('MessageSid', None)
            index = data.get('Index', None)
            date_created = data.get('DateCreated', None)
            body = data.get('Body', None)
            media = data.get('Media', None)
            author = data.get('Author', None)
            conversation_sid = data.get('ConversationSid', None)
            conversation = Conversation.objects.get(
                sid=conversation_sid,
            )
            Message.objects.create(
                sid=sid,
                index=index,
                date_created=date_created,
                body=body,
                author=author,
                conversation=conversation,
                media=media,
            )
        # case 'onParticipantUpdated':
        #     Participant.objects.filter(
        #         participant_sid=data['ParticipantSid'],
        #     ).update(
        #         last_read_message_index=data['LastReadMessageIndex'],
        #         last_read_timestamp=data['DateUpdated'],
        #     )
        case 'onDeliveryUpdated':
            sid = data.get('DeliveryReceiptSid')
            conversation_sid = data.get('ConversationSid')
            message_sid = data.get('MessageSid')
            participant_sid = data.get('ParticipantSid')
            status = getattr(Receipt.STATUS, data['Status'])
            error_code = data.get('ErrorCode')
            date_created = data.get('DateCreated')
            date_updated = data.get('DateUpdated')
            conversation = Conversation.objects.get(
                sid=conversation_sid,
            )
            participant = Participant.objects.get(
                sid=participant_sid,
            )
            message = Message.objects.get(
                sid=message_sid,
            )
            defaults = {
                'conversation': conversation,
                'message': message,
                'participant': participant,
                'status': status,
                'error_code': error_code,
                'date_created': date_created,
                'date_updated': date_updated,
            }
            Receipt.objects.update_or_create(
                sid=sid,
                defaults=defaults,
            )
