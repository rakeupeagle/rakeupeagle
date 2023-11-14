
# Django
from django.contrib import admin

# from .models import Message
# Local
from .models import Assignment
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


# class MessageInline(admin.TabularInline):
#     model = Message
#     fields = [
#         'id',
#         'direction',
#         'body',
#         'to_phone',
#         'from_phone',
#         'created',
#         'user',
#     ]
#     readonly_fields = [
#         'created',
#         'id',
#     ]
#     ordering = (
#         'created',
#     )
#     show_change_link = True
#     extra = 0
#     classes = [
#         # 'collapse',
#     ]
#     autocomplete_fields = [
#     ]


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
