from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Message
from .models import User
from .tasks import create_account_from_user
from .tasks import delete_user
from .tasks import send_text_from_message


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        create_account_from_user(instance)
    return

@receiver(pre_delete, sender=User)
def pre_delete_user(sender, instance, **kwargs):
    delete_user(instance.username)
    return

@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    if created and instance.direction == instance.DIRECTION.outbound:
        send_text_from_message.delay(instance)
    return
