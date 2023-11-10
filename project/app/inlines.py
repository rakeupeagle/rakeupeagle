
# Django
from django.contrib import admin

# Local
from .models import Assignment
from .models import Message
from .models import Rake
from .models import Recipient
from .models import Team
from .models import Yard


class AssignmentInline(admin.TabularInline):
    model = Assignment
    fields = [
        'yard',
        'rake',
    ]
    autocomplete_fields = [
        'yard',
        'rake',
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


class YardInline(admin.TabularInline):
    model = Yard
    fields = [
        'recipient',
        'state',
    ]
    autocomplete_fields = [
    ]
    extra = 0
    show_change_link = True


class RakeInline(admin.TabularInline):
    model = Rake
    fields = [
        'team',
        'state',
        'event',
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
