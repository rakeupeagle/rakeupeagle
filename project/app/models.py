from django.contrib.auth.models import AbstractBaseUser
from django.contrib.gis.db import models
from django.utils.safestring import mark_safe
from django_fsm import FSMIntegerField
# from django_fsm import transition
from hashid_field import HashidAutoField
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField

# Local
from .managers import UserManager


class Recipient(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (-10, 'exclude', 'Excluded'),
        (0, 'new', 'New'),
        (10, 'include', 'Included'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
    )
    SIZE = Choices(
        (110, 'small', 'Small (1-15 bags)'),
        (120, 'medium', 'Medium (16-30 bags)'),
        (130, 'large', 'Large (31+ bags)'),
    )
    size = models.IntegerField(
        blank=True,
        choices=SIZE,
        help_text="""Please provide the approximate yard size."""
    )
    location = models.CharField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Please provide the street address to be raked (City of Eagle is assumed)."""
    )
    address = models.CharField(
        max_length=512,
        blank=True,
        default='',
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
    bags = models.IntegerField(
        blank=True,
        null=True,
        help_text='Actual Bags Used',
    )
    hours = models.FloatField(
        blank=True,
        null=True,
        help_text='Actual Hours Worked',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    user = models.OneToOneField(
        'app.User',
        on_delete=models.CASCADE,
        related_name='recipient',
    )
    conversation = models.OneToOneField(
        'app.Conversation',
        on_delete=models.CASCADE,
        related_name='recipient',
        null=True,
        blank=True,
    )
    def __str__(self):
        return f"{self.user.name} - {self.get_size_display()}"

    # @transition(field=state, source=[STATE.new], target=STATE.confirmed)
    # def confirm(self):
    #     return


class Team(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (-10, 'exclude', 'Excluded'),
        (0, 'new', 'New'),
        (10, 'include', 'Included'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
    )
    SIZE = Choices(
        (105, 'solo', 'Solo (1 Adult)'),
        (110, 'xs', 'Extra-Small (2-5 Adults)'),
        (120, 'small', 'Small (6-10 Adults)'),
        (130, 'medium', 'Medium (11-15 Adults)'),
        (140, 'large', 'Large (16-20 Adults)'),
        (150, 'xl', 'Extra-Large (21+ Adults)'),
    )
    size = models.IntegerField(
        blank=False,
        choices=SIZE,
        help_text='The size of your group. (Number of adults, or equivalent in children.)',
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
    actual = models.IntegerField(
        blank=True,
        null=True,
        help_text='The actual number of adults, or adult-equivalent in children.',
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
    user = models.OneToOneField(
        'app.User',
        on_delete=models.CASCADE,
        related_name='team',
    )
    conversation = models.OneToOneField(
        'app.Conversation',
        on_delete=models.CASCADE,
        related_name='team',
        null=True,
        blank=True,
    )
    def __str__(self):
        return f"{self.user.name} - {self.nickname}"

    # @transition(field=state, source=[STATE.new,], target=STATE.confirmed)
    # def confirm(self):
    #     return


class Assignment(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (-30, 'incomplete', 'Incompleted'),
        (-20, 'fail', 'Failed'),
        (-10, 'cancel', 'Cancelled'),
        (0, 'new', 'New'),
        (20, 'confirm', 'Confirmed'),
        (30, 'checkin', 'Checked-In'),
        (40, 'start', 'Started'),
        (50, 'finish', 'Finished'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
    )
    TEAM_STATE = Choices(
        (-30, 'archived', 'Archived'),
        (-20, 'cancelled', 'Cancelled'),
        (-10, 'exclude', 'Excluded'),
        (0, 'new', 'New'),
        (10, 'include', 'Included'),
        (20, 'confirmed', 'Confirmed'),
        (30, 'checked', 'Checked-In'),
        (40, 'missed', 'Missed'),
        (50, 'complete', 'Complete'),
    )
    team_state = FSMIntegerField(
        choices=TEAM_STATE,
        default=TEAM_STATE.new,
    )
    RECIPIENT_STATE = Choices(
        (-40, 'blocked', 'Blocked'),
        (-30, 'archived', 'Archived'),
        (-20, 'cancelled', 'Cancelled'),
        (-10, 'exclude', 'Excluded'),
        (0, 'new', 'New'),
        (10, 'include', 'Included'),
        (20, 'confirmed', 'Confirmed'),
        (30, 'checked', 'Checked-In'),
        (40, 'missed', 'Missed'),
        (50, 'complete', 'Complete'),
    )
    recipient_state = FSMIntegerField(
        choices=RECIPIENT_STATE,
        default=RECIPIENT_STATE.new,
    )
    bags = models.IntegerField(
        blank=True,
        null=True,
        help_text='Actual Bags Used',
    )
    hours = models.FloatField(
        blank=True,
        null=True,
        help_text='Actual Hours Worked',
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
    yard = models.ForeignKey(
        'app.Yard',
        on_delete=models.CASCADE,
        related_name='assignments',
        null=True,
        blank=True,
    )
    rake = models.ForeignKey(
        'app.Rake',
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
    conversation = models.OneToOneField(
        'app.Conversation',
        on_delete=models.CASCADE,
        related_name='assignment',
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
        return f"{self.id}"


class Yard(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (-20, 'cancel', 'Cancelled'),
        (-10, 'exclude', 'Excluded'),
        (0, 'new', 'New'),
        (10, 'include', 'Included'),
        (20, 'confirm', 'Confirmed'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
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
        related_name='yards',
    )
    event = models.ForeignKey(
        'app.Event',
        on_delete=models.CASCADE,
        related_name='yards',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    def __str__(self):
        return f"{self.event.year} - {self.recipient.user.name} - {self.recipient.user.phone.as_national}"


class Rake(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (-20, 'cancel', 'Cancelled'),
        (-10, 'exclude', 'Excluded'),
        (0, 'new', 'New'),
        (10, 'include', 'Included'),
        (20, 'confirm', 'Confirmed'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
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
    team = models.ForeignKey(
        'app.Team',
        on_delete=models.CASCADE,
        related_name='rakes',
        null=True,
    )
    event = models.ForeignKey(
        'app.Event',
        on_delete=models.CASCADE,
        related_name='rakes',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    def __str__(self):
        return f"{self.event.year} - {self.team.user.name} - {self.team.user.phone.as_national}"


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
    STATE = Choices(
        (-10, 'archive', 'Archive'),
        (0, 'new', 'New'),
        (10, 'current', 'Current'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
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


class MessageArchive(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (0, 'new', 'New'),
        (10, 'sent', 'Sent'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
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
    DIRECTION = Choices(
        (10, 'inbound', 'Inbound'),
        (20, 'outbound', 'Outbound'),
    )
    direction = models.IntegerField(
        choices=DIRECTION,
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
        # related_name='messages',
    )
    def __str__(self):
        return f"{self.id}"


class Picture(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    image = models.ImageField(
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )


# Twilio
class Conversation(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    sid = models.CharField(
        max_length=100,
        unique=True,
    )
    STATE = Choices(
        (10, 'active', 'active'),
        (-10, 'inactive', 'inactive'),
        (-20, 'closed', 'closed'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.active,
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        null=True,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        null=True,
    )
    def __str__(self):
        return f"{self.name}"


class Participant(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    sid = models.CharField(
        max_length=100,
        unique=True,
    )
    phone = PhoneNumberField(
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        null=True,
    )
    last_read_message_index = models.IntegerField(
        null=True,
        blank=True,
    )
    last_read_timestamp = models.DateTimeField(
        null=True,
        blank=True,
    )
    # messaging_binding = models.JSONField(
    #     max_length=2048,
    #     null=True,
    #     blank=True,
    # )
    # origination = PhoneNumberField(
    #     null=True,
    #     blank=True,
    # )
    # identity = models.CharField(
    #     max_length=100,
    #     null=True,
    #     blank=True,
    # )
    # attributes = models.JSONField(
    #     null=True,
    #     blank=True,
    # )
    # url = models.URLField(
    #     max_length=1024,
    #     null=True,
    #     blank=True,
    # )
    conversation = models.ForeignKey(
        'app.Conversation',
        on_delete=models.CASCADE,
        to_field='sid',
        db_column='conversation_sid',
        related_name='participants',
    )
    def __str__(self):
        return f"{self.id}"


class Message(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    sid = models.CharField(
        max_length=100,
        unique=True,
    )
    index = models.IntegerField(
        null=True,
        blank=True,
    )
    author = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    body = models.TextField(
        max_length=1600,
        null=True,
        blank=True,
    )
    media = models.JSONField(
        max_length=2048,
        null=True,
        blank=True,
    )
    delivery = models.JSONField(
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )
    # url = models.URLField(
    #     max_length=1024,
    #     null=True,
    #     blank=True,
    # )
    # links = models.JSONField(
    #     null=True,
    #     blank=True,
    # )
    # attributes = models.JSONField(
    #     null=True,
    #     blank=True,
    # )
    # participant_sid = models.CharField(
    #     max_length=100,
    #     null=True,
    #     blank=True,
    # )
    # conversation_sid = models.CharField(
    #     max_length=100,
    #     null=True,
    #     blank=True,
    # )
    # content_sid = models.CharField(
    #     max_length=100,
    #     null=True,
    #     blank=True,
    # )
    conversation = models.ForeignKey(
        'app.Conversation',
        on_delete=models.CASCADE,
        to_field='sid',
        db_column='conversation_sid',
        related_name='messages',
    )
    content = models.ForeignKey(
        'app.Content',
        on_delete=models.SET_NULL,
        related_name='messages',
        to_field='sid',
        db_column='content_sid',
        null=True,
        blank=True,
    )
    def __str__(self):
        return f"{self.id}"


class Receipt(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    sid = models.CharField(
        max_length=100,
        unique=True,
    )
    STATUS = Choices(
        (-20, 'failed', 'failed'),
        (-10, 'undelivered', 'undelivered'),
        (0, 'sent', 'sent'),
        (20, 'delivered', 'delivered'),
        (30, 'read', 'read'),
    )
    status = FSMIntegerField(
        choices=STATUS,
    )
    error_code = models.IntegerField(
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )
    # url = models.URLField(
    #     max_length=1024,
    #     null=True,
    #     blank=True,
    # )
    # conversation_sid = models.CharField(
    #     max_length=100,
    #     null=True,
    # )
    # message_sid = models.CharField(
    #     max_length=100,
    #     null=True,
    # )
    # participant_sid = models.CharField(
    #     max_length=100,
    #     null=True,
    # )
    message = models.ForeignKey(
        'app.Message',
        on_delete=models.CASCADE,
        to_field='sid',
        db_column='message_sid',
        related_name='receipts',
    )
    participant = models.ForeignKey(
        'app.Participant',
        on_delete=models.CASCADE,
        to_field='sid',
        db_column='participation_sid',
        related_name='receipts',
    )
    conversation = models.ForeignKey(
        'app.Conversation',
        on_delete=models.CASCADE,
        to_field='sid',
        db_column='conversation_sid',
        related_name='receipts',
    )

    def __str__(self):
        return f"{self.id}"


class Content(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    sid = models.CharField(
        max_length=100,
        unique=True,
    )
    STATUS = Choices(
        (0, 'new', 'New'),
        (10, 'active', 'Active'),
    )
    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    body = models.CharField(
        max_length=1600,
        blank=True,
        default='',
    )
    components = models.JSONField(
        blank=True,
        null=True,
    )
    variables = models.JSONField(
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )
    def __str__(self):
        return str(self.name)


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
