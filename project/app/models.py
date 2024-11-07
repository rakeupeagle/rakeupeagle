import datetime

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.gis.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.safestring import mark_safe
from django_fsm import FSMIntegerField
from django_fsm import transition
# from fsm_admin2.admin import FSMTransitionMixin
from hashid_field import HashidAutoField
from phonenumber_field.modelfields import PhoneNumberField

from .choices import AssignmentStateChoices
from .choices import DirectionChoices
from .choices import EventStateChoices
from .choices import MessageStateChoices
from .choices import RecipientSizeChoices
from .choices import RecipientStateChoices
from .choices import TeamSizeChoices
from .choices import TeamStateChoices
# from .helpers import send_message
# Local
from .managers import UserManager
from .tasks import create_instance_message
from .tasks import create_recipients_message
from .tasks import create_teams_message
from .tasks import send_message


class Recipient(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    state = FSMIntegerField(
        choices=RecipientStateChoices,
        default=RecipientStateChoices.NEW,
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="""Your full name."""
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        unique=False,
        help_text="""Your mobile number."""
    )
    size = models.IntegerField(
        blank=False,
        choices=RecipientSizeChoices,
        help_text="""Please provide the approximate yard size."""
    )
    bags = models.IntegerField(
        blank=True,
        null=True,
        help_text='Bags estimate',
    )
    location = models.CharField(
        max_length=512,
        blank=False,
        default='',
    )
    place_id = models.CharField(
        max_length=512,
        null=True,
        blank=True,
    )
    point = models.PointField(
        null=True,
        blank=True,
    )
    is_senior = models.BooleanField(
        default=False,
    )
    is_disabled = models.BooleanField(
        default=False,
    )
    is_veteran = models.BooleanField(
        default=False,
    )
    is_dog = models.BooleanField(
        blank=True,
        default=False,
        help_text=mark_safe("""If you have a dog, it must be contained in your home for us to rake. <em>Also, you must clean up all animal waste before we arrive or our team group will not be able to rake.</em>"""),
    )
    notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Administrator Notes (from calling).""",
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    event = models.ForeignKey(
        'app.Event',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipients',
    )
    user = models.ForeignKey(
        'app.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='recipients',
    )

    @property
    def is_unread(self):
        return self.messages.filter(
            state=0,
        )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    'place_id',
                    'event',
                ],
                name='unique_location_event',
            ),
        ]
        ordering = (
            '-created',
        )

    def __str__(self):
        return f"{self.name}"

    @transition(
        field=state,
        source=[
            # RecipientStateChoices.NEW,
        ],
        target=RecipientStateChoices.INVITED,
    )
    def invite(self):
        create_instance_message(self, 'recipient_invited')
        return


    @transition(
        field=state,
        source=[
            RecipientStateChoices.NEW,
            RecipientStateChoices.INVITED,
        ],
        target=RecipientStateChoices.ACCEPTED,
    )
    def accept(self):
        create_instance_message(self, 'recipient_accepted')
        return


    @transition(
        field=state,
        source=[
            RecipientStateChoices.NEW,
            RecipientStateChoices.INVITED,
            RecipientStateChoices.ACCEPTED,
        ],
        target=RecipientStateChoices.DECLINED,
        conditions=[
            lambda x : x.event.state == EventStateChoices.CURRENT,
        ],
    )
    def decline(self):
        create_instance_message(self, 'recipient_declined')
        return


    @transition(
        field=state,
        source=[
            RecipientStateChoices.ACCEPTED,
        ],
        target=RecipientStateChoices.CONFIRMED,
    )
    def confirm(self):
        create_instance_message(self, 'recipient_confirmed')
        return


    @transition(
        field=state,
        source=[
            RecipientStateChoices.ACCEPTED,
            RecipientStateChoices.CONFIRMED,
        ],
        target=RecipientStateChoices.CANCELLED,
        conditions=[
            lambda x : x.event.state == EventStateChoices.CLOSED,
        ],
    )
    def cancel(self):
        create_instance_message(self, 'recipient_cancelled')
        return


    @transition(
        field=state,
        source=[
            RecipientStateChoices.CONFIRMED,
        ],
        target=RecipientStateChoices.ASSIGNED,
    )
    def assign(self):
        create_instance_message(self, 'team_assigned')
        return

    @transition(
        field=state,
        source=[
            RecipientStateChoices.CONFIRMED,
            RecipientStateChoices.ASSIGNED,
        ],
        target=RecipientStateChoices.COMPLETED,
    )
    def complete(self):
        return


class Team(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    state = FSMIntegerField(
        choices=TeamStateChoices,
        default=TeamStateChoices.NEW,
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="""Your full name."""
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        unique=False,
        help_text="""Your mobile number."""
    )
    size = models.IntegerField(
        blank=False,
        choices=TeamSizeChoices,
        help_text='The size of your group. (Number of adults, or equivalent in children.)',
    )
    adults = models.IntegerField(
        blank=True,
        null=True,
        help_text='The actual number of adults, or adult-equivalent in children.',
    )
    nickname = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="""Whimsical Team Name (ie, Robert's Rakers, Covey Courters, etc.)""",
    )
    reference = models.CharField(
        max_length=512,
        blank=True,
        default='',
        help_text="""How did you hear about us?""",
    )
    notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Administrator Notes (from calling).""",
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    event = models.ForeignKey(
        'app.Event',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teams',
    )
    user = models.ForeignKey(
        'app.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='teams',
    )

    @property
    def is_unread(self):
        return self.messages.filter(
            state=0,
        )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    'phone',
                    'event',
                ],
                name='unique_team_event',
            ),
        ]
        ordering = (
            '-created',
        )

    def __str__(self):
        return f"{self.name} - {self.event.year}"

    @transition(
        field=state,
        source=[
            # TeamStateChoices.NEW,
        ],
        target=TeamStateChoices.INVITED,
    )
    def invite(self):
        create_instance_message(self, 'team_invited')
        return


    @transition(
        field=state,
        source=[
            TeamStateChoices.NEW,
            TeamStateChoices.INVITED,
            TeamStateChoices.DECLINED,
        ],
        target=TeamStateChoices.ACCEPTED,
    )
    def accept(self):
        create_instance_message(self, 'team_accepted')
        return


    @transition(
        field=state,
        source=[
            TeamStateChoices.NEW,
            TeamStateChoices.INVITED,
            TeamStateChoices.ACCEPTED,
        ],
        target=TeamStateChoices.DECLINED,
        conditions=[
            lambda x : x.event.state == EventStateChoices.CURRENT,
        ],
    )
    def decline(self):
        create_instance_message(self, 'team_declined')
        return


    @transition(
        field=state,
        source=[
            TeamStateChoices.ACCEPTED,
        ],
        target=TeamStateChoices.CONFIRMED,
    )
    def confirm(self):
        create_instance_message(self, 'team_confirmed')
        return


    @transition(
        field=state,
        source=[
            TeamStateChoices.ACCEPTED,
            TeamStateChoices.CONFIRMED,
        ],
        target=TeamStateChoices.CANCELLED,
        conditions=[
            lambda x : x.event.state == EventStateChoices.CLOSED,
        ],
    )
    def cancel(self):
        create_instance_message(self, 'team_cancelled')
        return


    @transition(
        field=state,
        source=[
            TeamStateChoices.CONFIRMED,
        ],
        target=TeamStateChoices.ASSIGNED,
    )
    def assign(self):
        create_instance_message(self, 'team_assigned')
        return


    @transition(
        field=state,
        source=[
            TeamStateChoices.CONFIRMED,
            TeamStateChoices.ASSIGNED,
        ],
        target=TeamStateChoices.COMPLETED,
    )
    def complete(self):
        return


class Message(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    state = FSMIntegerField(
        choices=MessageStateChoices,
        default=MessageStateChoices.NEW,
    )
    sid = models.CharField(
        max_length=100,
        blank=True,
        unique=True,
        null=True,
    )
    is_read = models.BooleanField(
        default=False,
    )
    to_phone = PhoneNumberField(
        blank=True,
        null=True,
    )
    from_phone = PhoneNumberField(
        blank=True,
        null=True,
    )
    body = models.TextField(
        blank=False,
    )
    direction = models.IntegerField(
        choices=DirectionChoices,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    user = models.ForeignKey(
        'app.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='messages',
    )
    recipient = models.ForeignKey(
        'app.Recipient',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
    )
    team = models.ForeignKey(
        'app.Team',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
    )
    def __str__(self):
        return f"{self.id}"

    @transition(
        field=state,
        source=[
            MessageStateChoices.NEW,
        ],
        target=MessageStateChoices.READ,
        conditions=[
            lambda x : x.direction == DirectionChoices.INBOUND,
        ]
    )
    def read(self):
        return


    @transition(
        field=state,
        source=[
            MessageStateChoices.NEW,
        ],
        target=MessageStateChoices.SENT,
        conditions=[
            lambda x : x.direction == DirectionChoices.OUTBOUND,
            lambda x : not x.sid,
        ]
    )
    def send(self):
        response = send_message.delay(self)
        return


class Event(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="""Your full name."""
    )
    state = FSMIntegerField(
        choices=EventStateChoices,
        default=EventStateChoices.NEW,
    )
    year = models.IntegerField(
        blank=True,
        null=True,
    )
    notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Please add any other notes you think we should know.""",
    )
    date =  models.DateField(
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    @property
    def deadline(self):
        return self.date - datetime.timedelta(days=4)

    @transition(
        field=state,
        source=[
            EventStateChoices.CURRENT,
        ],
        target=EventStateChoices.CLOSED,
        conditions=[
            lambda x: x.date >= datetime.date.today()
        ]
    )
    def close(self):
        create_recipients_message(self, 'recipient_confirmation')
        create_teams_message(self, 'team_confirmation')
        return


    def __str__(self):
        return f"{self.year}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    'year',
                ],
                name='unique_event_year',
            ),
        ]
        ordering = (
            '-year',
        )


class Assignment(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    state = FSMIntegerField(
        choices=AssignmentStateChoices,
        default=AssignmentStateChoices.NEW,
    )
    notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Internal (private) notes.""",
    )
    recipient = models.ForeignKey(
        'app.Recipient',
        on_delete=models.CASCADE,
        related_name='assignments',
        null=True,
        blank=True,
    )
    team = models.ForeignKey(
        'app.Team',
        on_delete=models.CASCADE,
        related_name='assignments',
        null=True,
        blank=True,
    )
    event = models.ForeignKey(
        'app.Event',
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    def __str__(self):
        return f"{self.id}"


class User(AbstractBaseUser):
    id = HashidAutoField(
        primary_key=True,
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        unique=True,
    )
    name = models.CharField(
        max_length=150,
        blank=True,
        null=False,
        default='',
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_verified = models.BooleanField(
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

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = [
        'phone',
    ]

    objects = UserManager()

    class Meta:
        ordering = (
            'phone',
        )


    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return f"{self.phone} - {self.name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
