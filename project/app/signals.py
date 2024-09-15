from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .helpers import create_message
from .helpers import delete_message
from .models import Message


@receiver(pre_save, sender=Message)
def message_pre_save(sender, instance, **kwargs):
    # create_message(instance)
    return

# @receiver(pre_delete, sender=Message)
# def message_pre_delete(sender, instance, **kwargs):
#     delete_message(instance)
#     return
