# Django
from django.contrib.auth.backends import ModelBackend

# Local
from .models import User


class AppBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        phone = kwargs.get('phone')
        name = kwargs.get('name', '')
        try:
            user = User.objects.get(
                phone=phone,
            )
        except User.DoesNotExist:
            user = User.objects.create_user(
                phone=phone,
                name=name,
            )
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
