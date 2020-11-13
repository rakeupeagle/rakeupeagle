# Django
from django.contrib.auth.models import AbstractBaseUser
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

# First-Party
from hashid_field import HashidAutoField
from model_utils import Choices
from phone_field import PhoneField

# Local
from .managers import UserManager


class Recipient(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    SIZE = Choices(
        (110, 'small', 'Small (1-15 bags)'),
        (120, 'medium', 'Medium (16-30 bags)'),
        (130, 'large', 'Large (35+ bags)'),
    )
    size = models.IntegerField(
        blank=False,
        choices=SIZE,
        help_text='Yard Size',
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
    geo = models.JSONField(
        encoder=DjangoJSONEncoder,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        blank=False,
        help_text="""Your email.""",
        default='',
    )
    phone = PhoneField(
        max_length=255,
        blank=False,
        help_text="""Your phone.""",
        default='',
    )
    is_verified = models.BooleanField(
        blank=False,
        help_text="""We are only able to service yards for persons in one of these categories.""",
    )
    is_dog = models.BooleanField(
        blank=False,
        help_text="""If you have a dog, it must be contained in your home for us to rake.  Also, you must clean up all animal waste before we arrive or our volunteer group will not be able to rake.""",
    )
    is_waiver = models.BooleanField(
        help_text='I agree to waive and release Rake Up Eagle and the sponsors of this event, including all persons and agencies connected with this event from all claims for damages, injuries or death, arising from my participation in  this event. I will provide my own insurance and care, if necessary. I also understand and agree that Rake Up Eagle or a sponsor may subsequently use for publicity and/or promotional purposes pictures of me and my team participating in this event without obligation of liability to me. I understand that the work done on my property is done by volunteers and will not hold them or Rake Up Eagle responsible for damage to personal property. I have read this waiver carefully and having done so, I am signing voluntarily.',
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

    def is_assigned(self):
        return bool(self.assignments.count())

    def __str__(self):
        return " - ".join([
            str(self.name),
            str(self.get_size_display()),
        ])

    @property
    def total(self):
        return self.volunteers.aggregate(
            s=models.Sum('number')
        )['s']

    @property
    def reps(self):
        return "; ".join(
            self.volunteers.values_list('name', flat=True)
        )

class Volunteer(models.Model):
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
    phone = PhoneField(
        max_length=255,
        blank=False,
        help_text="""Your mobile phone.""",
        default='',
    )
    number = models.IntegerField(
        blank=False,
        null=True,
        help_text="""Number in your group.""",
    )
    adults = models.IntegerField(
        blank=True,
        null=True,
        help_text="""Number of adults in your group.""",
    )
    children = models.IntegerField(
        blank=True,
        null=True,
        help_text="""Number of children in your group.""",
    )
    recipient = models.ForeignKey(
        'Recipient',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='volunteers',
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

    def is_assigned(self):
        return bool(self.assignments.count())

    def __str__(self):
        return "{0} - {1} Persons".format(
            str(self.name),
            str(self.number),
        )


# class Assignment(models.Model):
#     id = HashidAutoField(
#         primary_key=True,
#     )
#     STATUS = Choices(
#         (0, 'new', "New"),
#         (10, 'pending', "Pending"),
#         (20, 'accepted', "Accepted"),
#         (30, 'rejected', "Rejected"),
#     )
#     status = models.IntegerField(
#         blank=True,
#         choices=STATUS,
#         default=STATUS.new,
#     )
#     notes = models.TextField(
#         blank=True,
#         default='',
#     )
#     recipient = models.ForeignKey(
#         'Recipient',
#         on_delete=models.CASCADE,
#         blank=False,
#         related_name='assignments',
#     )
#     volunteer = models.ForeignKey(
#         'Volunteer',
#         on_delete=models.CASCADE,
#         blank=False,
#         related_name='assignments',
#     )
#     notes = models.TextField(
#         max_length=512,
#         blank=True,
#         default='',
#         help_text="""Notes.""",
#     )
#     created = models.DateTimeField(
#         auto_now_add=True,
#     )
#     updated = models.DateTimeField(
#         auto_now=True,
#     )

#     def __str__(self):
#         return " : ".join([
#             str(self.recipient),
#             str(self.volunteer),
#         ])

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=[
#                     'recipient',
#                     'volunteer',
#                 ],
#                 name='unique_assignment',
#             ),
#         ]


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
        'email',
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
