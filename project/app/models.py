# # Django
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from hashid_field import HashidAutoField
from model_utils import Choices

# # Local
from .managers import UserManager


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
    email = models.EmailField(
        max_length=255,
        blank=False,
        help_text="""Your email address.""",
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
        help_text="""Number in your group.""",
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
        return str(self.name)


class Recipient(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    SIZE = Choices(
        (110, 'small', 'Small (1-15 bags)'),
        (120, 'medium', 'Medium (16-30 bags'),
        (130, 'large', 'Large (35+ bags)'),
    )
    size = models.IntegerField(
        blank=False,
        choices=SIZE,
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        help_text="""Your name.""",
        default='',
    )
    address = models.CharField(
        max_length=255,
        blank=False,
        help_text="""Your street address (must be in Eagle).""",
        default='',
    )
    email = models.EmailField(
        blank=False,
        help_text="""Your email.""",
        default='',
    )
    phone = models.CharField(
        max_length=255,
        blank=False,
        help_text="""Your phone.""",
        default='',
    )
    is_verified = models.BooleanField(
        blank=False,
        help_text="""Are you age 65 or older, disabled, or veteran?""",
    )
    is_dog = models.BooleanField(
        blank=False,
        help_text="""Do you have a dog?""",
    )
    is_waiver = models.BooleanField(
        blank=False,
    )
    notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Please add any other notes you think we should know.""",
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
        related_name='location',
        null=True,
    )
    def __str__(self):
        return str(self.name)


class Assignment(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATUS = Choices(
        (0, 'new', "New"),
        (10, 'pending', "Pending"),
        (20, 'accepted', "Accepted"),
        (30, 'rejected', "Rejected"),
    )
    status = models.IntegerField(
        blank=True,
        choices=STATUS,
        default=STATUS.new,
    )
    notes = models.TextField(
        blank=True,
        default='',
    )
    recipient = models.ForeignKey(
        'Recipient',
        on_delete=models.CASCADE,
        blank=False,
        related_name='recipients',
    )
    volunteer = models.ForeignKey(
        'Volunteer',
        on_delete=models.CASCADE,
        blank=False,
        related_name='volunteers',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )


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