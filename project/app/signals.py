from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import User
from .tasks import delete_user


@receiver(pre_delete, sender=User)
def pre_delete_user(sender, instance, **kwargs):
    delete_user(instance.username)
