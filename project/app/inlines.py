
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
