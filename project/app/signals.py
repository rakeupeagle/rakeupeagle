# # Django
# from django.db.models.signals import post_delete
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# # First-Party
# from app.models import Account
# from app.models import Parent
# from app.models import Student
# from app.models import Teacher
# from app.models import User
# from app.tasks import auth0_delete_user
# from app.tasks import build_email
# from app.tasks import mailchimp_create_or_update_from_user
# from app.tasks import mailchimp_delete_email
# from app.tasks import send_email


# @receiver(post_delete, sender=User)
# def user_post_delete(sender, instance, **kwargs):
#     user = instance
#     auth0_delete_user(user.username)
#     result = mailchimp_delete_email.delay(user.email)
#     # email = build_email(
#     #     to=[user.email],
#     #     subject='Start Normal - Account Deleted',
#     #     template='emails/delete.txt',
#     #     bcc=['dbinetti@startnormal.com'],
#     # )
#     # send_email.delay(email)
#     return


# @receiver(post_save, sender=User)
# def user_post_save(sender, instance, created, raw=False, **kwargs):
#     if created and not raw:
#         Account.objects.create(
#             user=instance,
#         )
#         mailchimp_create_or_update_from_user.delay(instance)
#         try:
#             parent = Parent.objects.get(
#                 email=instance.email,
#             )
#         except Parent.DoesNotExist:
#             return
#         parent.user = instance
#         parent.save()
#     return


# @receiver(post_save, sender=Student)
# def student_post_save(sender, instance, created, raw=False, **kwargs):
#     if created and not raw:
#         instance = instance._meta.default_manager.with_vector().get(pk=instance.pk)
#         instance.search_vector = instance.vector
#         instance.save()
#     return
