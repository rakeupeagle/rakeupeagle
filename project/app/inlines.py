
# Django
from django.contrib import admin

# Local
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
