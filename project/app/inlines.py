
# Django
from django.contrib import admin

# Local
from .models import Assignment
from .models import Conversation
from .models import Message
from .models import MessageArchive
from .models import Participant
from .models import Receipt
from .models import Recipient
from .models import Team


class AssignmentInline(admin.TabularInline):
    model = Assignment
    fields = [
        'recipient',
        'team',
    ]
    autocomplete_fields = [
        'recipient',
        'team',
    ]
    extra = 0
    show_change_link = True



class TeamInline(admin.TabularInline):
    model = Team
    fields = [
        'size',
    ]
    autocomplete_fields = [
    ]
    extra = 0
    show_change_link = True


class MessageArchiveInline(admin.TabularInline):
    model = MessageArchive
    fields = [
        'id',
        'direction',
        'body',
        'to_phone',
        'from_phone',
        'created',
        'user',
    ]
    readonly_fields = [
        'created',
        'id',
    ]
    ordering = (
        'created',
    )
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]
    autocomplete_fields = [
    ]


class RecipientInline(admin.TabularInline):
    model = Recipient
    fields = [
        # 'status',
        'size',
        'location',
        'is_dog',
    ]
    autocomplete_fields = [
    ]
    extra = 0
    show_change_link = True


# Twilio
class ConversationInline(admin.TabularInline):
    model = Conversation
    fields = [
        # 'identity',
        'state',
        'date_created',
        'date_updated',
        # 'messaging_binding',
        # 'user',
    ]
    readonly_fields = [
        # 'identity',
        'date_created',
        'date_updated',
        # 'conversation',
    ]
    ordering = (
    )
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]
    autocomplete_fields = [
        # 'user',
    ]


class ParticipantInline(admin.TabularInline):
    model = Participant
    fields = [
        # 'identity',
        'phone',
        'last_read_message_index',
        'last_read_timestamp',
        'date_created',
        'date_updated',
        # 'messaging_binding',
        'conversation',
    ]
    readonly_fields = [
        # 'identity',
        'date_created',
        'date_updated',
        'last_read_message_index',
        'last_read_timestamp',
        # 'conversation',
    ]
    ordering = (
    )
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]
    autocomplete_fields = [
        'conversation',
    ]


class MessageInline(admin.TabularInline):
    model = Message
    fields = [
        # 'content',
        'author',
        'body',
        # 'media',
        # 'attributes',
        'date_created',
        'date_updated',
        # 'delivery',
        'conversation',
    ]
    readonly_fields = [
        'index',
        # 'author',
        # 'body',
        # 'media',
        # 'attributes',
        'date_created',
        'date_updated',
        # 'delivery',
        'conversation',
    ]
    ordering = (
        'index',
    )
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]
    autocomplete_fields = [
        # 'content',
    ]


class ReceiptInline(admin.TabularInline):
    model = Receipt
    fields = [
        'status',
        'error_code',
        'date_created',
        'date_updated',
        'participant',
        'message',
        'conversation',
    ]
    readonly_fields = [
    ]
    ordering = (
    )
    show_change_link = True
    extra = 0
    classes = [
        # 'collapse',
    ]
    readonly_fields = [
        'status',
        'error_code',
        'date_created',
        'date_updated',
        'participant',
        'message',
        'conversation',
    ]
