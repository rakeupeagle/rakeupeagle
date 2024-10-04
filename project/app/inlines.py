
from django.conf import settings
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
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['direction'].initial = Message.DirectionChoices.OUTBOUND
        formset.form.base_fields['to_phone'].initial = obj.phone
        formset.form.base_fields['from_phone'].initial = settings.TWILIO_NUMBER
        return formset


class RecipientMessageInline(admin.TabularInline):
    model = Message
    fields = [
        'id',
        'direction',
        'body',
        'created',
        'recipient',
        'state',
        'to_phone',
        'from_phone',
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
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['direction'].initial = Message.DirectionChoices.OUTBOUND
        formset.form.base_fields['to_phone'].initial = obj.phone
        formset.form.base_fields['from_phone'].initial = settings.TWILIO_NUMBER
        return formset


class TeamMessageInline(admin.TabularInline):
    model = Message
    fields = [
        'id',
        'direction',
        'body',
        'created',
        'team',
        'state',
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
