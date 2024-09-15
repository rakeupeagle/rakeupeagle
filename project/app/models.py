from django.contrib.auth.models import AbstractBaseUser
from django.contrib.gis.db import models
from django.db.models import IntegerChoices
from django.db.models.constraints import UniqueConstraint
from django.utils.safestring import mark_safe
from django_fsm import FSMIntegerField
# from django_fsm import transition
from hashid_field import HashidAutoField
from phonenumber_field.modelfields import PhoneNumberField

# Local
from .managers import UserManager


class Recipient(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    class StateChoices(IntegerChoices):
        BLOCKED = -40, "Blocked"
        CANCELLED = -20, "Cancelled"
        INACTIVE = -10, "Inactive"
        NEW = 0, "New"
        ACTIVE = 10, "Active"
        CONFIRMED = 20, "Confirmed"
        ASSIGNED = 30, "Assigned"
    state = FSMIntegerField(
        choices=StateChoices,
        default=StateChoices.NEW,
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
    class SizeChoices(IntegerChoices):
        SMALL = 110, "Small (1-15 bags)"
        MEDIUM = 120, "Medium (16-30 bags)"
        LARGE = 130, "Large (31+ bags)"
    size = models.IntegerField(
        blank=False,
        choices=SizeChoices,
        help_text="""Please provide the approximate yard size."""
    )
    bags = models.IntegerField(
        blank=True,
        null=True,
        help_text='Bags estimate',
    )
    location = models.CharField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Please provide the street address to be raked (City of Eagle is assumed)."""
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
    public_notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Please add any other notes you think we should know.""",
    )
    admin_notes = models.TextField(
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
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    'phone',
                    'event',
                ],
                name='unique_recipient_event',
            ),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_size_display()}"

    # @transition(field=state, source=[STATE.new], target=STATE.confirmed)
    # def confirm(self):
    #     return


class Team(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    class StateChoices(IntegerChoices):
        CANCELLED = -20, "Cancelled"
        INACTIVE = -10, "Inactive"
        NEW = 0, "New"
        ACTIVE = 10, "Active"
        CONFIRMED = 20, "Confirmed"
        ASSIGNED = 30, "Assigned"

    class SizeChoices(IntegerChoices):
        SOLO = 105, "Solo (1 Adult)"
        XSMALL = 110, "Extra-Small (2-5 Adults)"
        SMALL = 120, "Small (6-10 Adults)"
        MEDIUM = 130, "Medium (11-15 Adults)"
        LARGE = 140, "Large (16-20 Adults)"
        XLARGE = 150, "Extra-Large (21+ Adults)"

    state = FSMIntegerField(
        choices=StateChoices,
        default=StateChoices.NEW,
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
        choices=SizeChoices,
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
    public_notes = models.TextField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Notes.""",
    )
    admin_notes = models.TextField(
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

    def __str__(self):
        return f"{self.name} - {self.nickname}"

    # @transition(field=state, source=[STATE.new,], target=STATE.confirmed)
    # def confirm(self):
    #     return


class Assignment(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    class StateChoices(IntegerChoices):
        FAILED = -20, "Failed"
        CANCELLED = -10, "Cancelled"
        NEW = 0, "New"
        ASSIGNED = 10, "Assigned"
        STARTED = 40, "Started"
        FINISHED = 50, "Finished"

    state = FSMIntegerField(
        choices=StateChoices,
        default=StateChoices.NEW,
    )
    public_notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Please add any other notes you think we should know.""",
    )
    admin_notes = models.TextField(
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


class Event(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    class StateChoices(IntegerChoices):
        ARCHIVE = -10, "Archive"
        NEW = 0, "New"
        CURRENT = 10, "Current"

    name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="""Your full name."""
    )
    state = FSMIntegerField(
        choices=StateChoices,
        default=StateChoices.NEW,
    )
    year = models.IntegerField(
        blank=True,
        null=True
    )
    admin_notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Please add any other notes you think we should know.""",
    )
    deadline =  models.DateField(
        null=True,
        blank=True,
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
    def __str__(self):
        return f"{self.year}"


class Message(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    class StateChoices(IntegerChoices):
        NEW = 0, "New"
        SENT = 10, "Sent"

    class DirectionChoices(IntegerChoices):
        INBOUND = 10, "Inbound"
        OUTBOUND = 20, "Outbound"

    state = FSMIntegerField(
        choices=StateChoices,
        default=StateChoices.NEW,
    )
    sid = models.CharField(
        max_length=100,
        blank=True,
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
        blank=True,
    )
    direction = models.IntegerField(
        choices=DirectionChoices,
        null=True,
        blank=True,
    )
    raw = models.JSONField(
        blank=True,
        null=True,
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
