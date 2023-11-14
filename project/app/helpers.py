import logging

from django.conf import settings
from django_rq import job
from twilio.rest import Client as TwilioClient

# from .models import Message

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
    return

@job('default')
def delete_message(message):
    return


def process_webhook(data):
    return
    # log.info(data)
    # event_type = data['EventType']
    # match event_type:
    #     # case 'onConversationStateUpdated':
    #     #     Conversation.objects.filter(
    #     #         sid=data['ConversationSid'],
    #     #     ).update(
    #     #         state=getattr(Conversation.STATE, data['StateTo']),
    #     #     )
    #     # case 'onParticipantAdded':
    #     #     Participant.objects.create(
    #     #         sid=data['ParticipantSid'],
    #     #         conversation_sid=data['ConversationSid'],
    #     #         phone=data['MessagingBinding.Address'],
    #     #         date_created=data['DateCreated'],
    #     #     )
    #     case 'onMessageAdded':
    #         sid = data.get('MessageSid', None)
    #         index = data.get('Index', None)
    #         date_created = data.get('DateCreated', None)
    #         body = data.get('Body', None)
    #         media = data.get('Media', None)
    #         author = data.get('Author', None)
    #         conversation_sid = data.get('ConversationSid', None)
    #         conversation = Conversation.objects.get(
    #             sid=conversation_sid,
    #         )
    #         Message.objects.create(
    #             sid=sid,
    #             index=index,
    #             date_created=date_created,
    #             body=body,
    #             author=author,
    #             conversation=conversation,
    #             media=media,
    #         )
    #     # case 'onParticipantUpdated':
    #     #     Participant.objects.filter(
    #     #         participant_sid=data['ParticipantSid'],
    #     #     ).update(
    #     #         last_read_message_index=data['LastReadMessageIndex'],
    #     #         last_read_timestamp=data['DateUpdated'],
    #     #     )
    #     case 'onDeliveryUpdated':
    #         sid = data.get('DeliveryReceiptSid')
    #         conversation_sid = data.get('ConversationSid')
    #         message_sid = data.get('MessageSid')
    #         participant_sid = data.get('ParticipantSid')
    #         status = getattr(Receipt.STATUS, data['Status'])
    #         error_code = data.get('ErrorCode')
    #         date_created = data.get('DateCreated')
    #         date_updated = data.get('DateUpdated')
    #         conversation = Conversation.objects.get(
    #             sid=conversation_sid,
    #         )
    #         participant = Participant.objects.get(
    #             sid=participant_sid,
    #         )
    #         message = Message.objects.get(
    #             sid=message_sid,
    #         )
    #         defaults = {
    #             'conversation': conversation,
    #             'message': message,
    #             'participant': participant,
    #             'status': status,
    #             'error_code': error_code,
    #             'date_created': date_created,
    #             'date_updated': date_updated,
    #         }
    #         Receipt.objects.update_or_create(
    #             sid=sid,
    #             defaults=defaults,
    #         )
