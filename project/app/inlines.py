
# Django
from django.contrib import admin

# Local
from .models import Assignment
from .models import Message
from .models import Recipient
from .models import Volunteer


class AssignmentInline(admin.TabularInline):
    model = Assignment
    fields = [
        'recipient',
        'volunteer',
    ]
    autocomplete_fields = [
        'recipient',
        'volunteer',
    ]
    extra = 0
    show_change_link = True


class VolunteerInline(admin.TabularInline):
    model = Volunteer
    fields = [
        'size',
    ]
    autocomplete_fields = [
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
