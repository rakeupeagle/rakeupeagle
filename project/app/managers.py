# # Django
# Django
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, name, phone, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', False)
        user = self.model(
            name=name,
            phone=phone,
            **extra_fields
        )
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, name, phone, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', False)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        return self.create_user(
            name,
            phone,
            **extra_fields,
        )
