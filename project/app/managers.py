# # Django
from django.contrib.auth.base_user import BaseUserManager

# from django.contrib.postgres.search import SearchVector
# from django.db.models import Case
# from django.db.models import CharField
# from django.db.models import Value
# from django.db.models import When


# class StudentManager(BaseUserManager):
#     def with_vector(self):
#         grades = [When(grade=k, then=Value(v)) for k, v in self.model.GRADE]
#         vector = \
#             SearchVector(
#                 'name',
#                 weight='A',
#             ) + \
#             SearchVector(
#                 'school__name',
#                 weight='B',
#             ) + \
#             SearchVector(
#                 Case(*grades, output_field=CharField()),
#                 weight='C',
#             ) + \
#             SearchVector(
#                 'parent__name',
#                 weight='B',
#             ) + \
#             SearchVector(
#                 'parent__email',
#                 weight='B',
#             )
#         return self.get_queryset().annotate(vector=vector)


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        # if not email:
        #     raise ValueError('The Email must be set')
        # email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        return self.create_user(username, password, **extra_fields)
