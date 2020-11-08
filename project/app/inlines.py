
# Django
from django.contrib import admin

# Local
from .models import Assignment


class AssignmentInline(admin.TabularInline):
    model = Assignment
    fields = [
        'status',
        'recipient',
        'volunteer',
    ]
    autocomplete_fields = [
        'recipient',
        'volunteer',
    ]
    extra = 0
    show_change_link = True
