from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .helpers import create_conversation
from .helpers import create_message
from .helpers import create_participant
from .helpers import delete_conversation
from .helpers import delete_message
from .helpers import delete_participant
from .models import Conversation
from .models import Message
from .models import Participant


@receiver(pre_save, sender=Conversation)
def conversation_pre_save(sender, instance, **kwargs):
    create_conversation(instance)
    return

@receiver(pre_delete, sender=Conversation)
def conversation_pre_delete(sender, instance, **kwargs):
    delete_conversation(instance)
    return

@receiver(pre_save, sender=Participant)
def participant_pre_save(sender, instance, **kwargs):
    create_participant(instance)
    return

@receiver(pre_delete, sender=Participant)
def participant_pre_delete(sender, instance, **kwargs):
    delete_participant(instance)
    return

# @receiver(pre_save, sender=Message)
# def message_pre_save(sender, instance, **kwargs):
#     create_message(instance)
#     return

# @receiver(pre_delete, sender=Message)
# def message_pre_delete(sender, instance, **kwargs):
#     delete_message(instance)
#     return
