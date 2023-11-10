from django.db.models.signals import post_save
from django.dispatch import receiver

# from .models import Message
# from .tasks import send_copy_from_message
# from .tasks import send_text_from_message


# @receiver(post_save, sender=Message)
# def message_post_save(sender, instance, created, **kwargs):
#     if created and instance.direction == instance.DIRECTION.outbound:
#         send_text_from_message.delay(instance)
#     if created and instance.direction == instance.DIRECTION.inbound:
#         send_copy_from_message.delay(instance)
#     return
