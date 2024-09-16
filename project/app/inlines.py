
# Django
from django.contrib import admin

# Local
from .models import Assignment
from .models import Message
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



class RecipientInline(admin.TabularInline):
    model = Recipient
    fields = [
        # 'status',
        'name',
        'phone',
        'size',
        'location',
        'event',
    ]
    autocomplete_fields = [
    ]
    extra = 0
    show_change_link = True


class TeamInline(admin.TabularInline):
    model = Team
    fields = [
        'name',
        'nickname',
        'phone',
        'size',
        'event',
    ]
    autocomplete_fields = [
    ]
    extra = 0
    show_change_link = True


class RecipientMessageInline(admin.TabularInline):
    model = Message
    fields = [
        'id',
        'direction',
        'body',
        'created',
        'recipient',
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
    ]
    autocomplete_fields = [
    ]


class TeamMessageInline(admin.TabularInline):
    model = Message
    fields = [
        'id',
        'direction',
        'body',
        'created',
        'team',
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
    ]
    autocomplete_fields = [
    ]


class UserMessageInline(admin.TabularInline):
    model = Message
    fields = [
        'id',
        'direction',
        'body',
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
    ]
    autocomplete_fields = [
    ]
