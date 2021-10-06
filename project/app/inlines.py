
# Django
from django.contrib import admin

# Local
from .models import Message
from .models import Recipient
from .models import Volunteer


class VolunteerInline(admin.TabularInline):
    model = Volunteer
    fields = [
        # 'status',
        'recipient',
        'name',
        'number',
    ]
    autocomplete_fields = [
        # 'recipient',
    ]
    extra = 0
    show_change_link = True


class MessageInline(admin.TabularInline):
    model = Message
    fields = [
        'id',
        'direction',
        'body',
        # 'to_phone',
        # 'from_phone',
        'created',
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
        'account',
    ]

class RecipientInline(admin.TabularInline):
    model = Recipient
    fields = [
        # 'status',
        'size',
        'is_dog',
        'notes',
        'account',
    ]
    autocomplete_fields = [
        'account',
    ]
    extra = 0
    show_change_link = True
