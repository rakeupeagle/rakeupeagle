# # Django
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from hashid_field import HashidAutoField
from model_utils import Choices

# # Local
from .managers import UserManager

# # First-Party



class Volunteer(models.Model):
    NUMBER = Choices(
        (1, 'one', "One"),
        (2, 'two', "Two"),
        (3, 'three', "Three"),
        (4, 'four', "Four"),
        (5, 'five', "Five +"),
    )
    id = HashidAutoField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        help_text="""Your name (or group name).""",
        default='',
    )
    phone = models.CharField(
        max_length=255,
        blank=False,
        help_text="""Your mobile phone.""",
        default='',
    )
    number = models.IntegerField(
        blank=False,
        choices=NUMBER,
        help_text="""Number in Group.""",
    )
    notes = models.TextField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Notes.""",
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    user = models.OneToOneField(
        'app.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='volunteer',
    )

    def __str__(self):
        return str(self.user)


# class Location(models.Model):
#     id = HashidAutoField(
#         primary_key=True,
#     )
#     SUBJECT = Choices(
#         (110, 'ps', 'English'),
#         (120, 'ps', 'History'),
#         (130, 'ps', 'Mathematics'),
#         (140, 'ps', 'Science'),
#         (150, 'ps', 'Art'),
#         (160, 'ps', 'Music'),
#         (170, 'ps', 'PE'),
#         (180, 'ps', 'Other'),
#     )
#     subject = models.IntegerField(
#         blank=False,
#         choices=SUBJECT,
#         default=SUBJECT.none
#     )
#     notes = models.TextField(
#         max_length=2000,
#         blank=True,
#         default='',
#         help_text="""Please add any other notes you think we should know.""",
#     )
#     created = models.DateTimeField(
#         auto_now_add=True,
#     )
#     updated = models.DateTimeField(
#         auto_now=True,
#     )
#     user = models.OneToOneField(
#         'app.User',
#         on_delete=models.CASCADE,
#         related_name='location',
#     )
#     def __str__(self):
#         return str(self.user)




class User(AbstractBaseUser):
    id = HashidAutoField(
        primary_key=True,
    )
    username = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
    )
    email = models.EmailField(
        blank=False,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
        blank=False,
    )
    is_active = models.BooleanField(
        default=False,
    )
    is_admin = models.BooleanField(
        default=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'name',
    ]

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return str(self.name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
