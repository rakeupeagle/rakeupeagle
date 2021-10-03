from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import User
from .tasks import delete_user
from .tasks import get_or_create_account_from_user


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    print(created)
    if created:
        get_or_create_account_from_user(instance)
    return

@receiver(pre_delete, sender=User)
def pre_delete_user(sender, instance, **kwargs):
    # delete_user(instance.username)
    return
