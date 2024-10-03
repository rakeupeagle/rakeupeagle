# Django
# First-Party
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.gis.admin.options import GISModelAdmin
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from fsm_admin.mixins import FSMTransitionMixin

from .actions import mark_read
from .actions import send_invitations
from .actions import send_message
from .filters import DirectionListFilter
# Local
# from .forms import AssignmentForm
from .forms import UserChangeForm
from .forms import UserCreationForm
# from .inlines import AssignmentInline
from .inlines import RecipientInline
from .inlines import RecipientMessageInline
from .inlines import TeamInline
from .inlines import TeamMessageInline
from .inlines import UserMessageInline
from .models import Assignment
from .models import Event
from .models import Message
from .models import Recipient
from .models import Team
from .models import User


@admin.register(Recipient)
class RecipientAdmin(FSMTransitionMixin, GISModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'phone',
        'state',
        'event',
        'location',
        'point',
        'size',
        'is_veteran',
        'is_senior',
        'is_disabled',
        'is_dog',
        'bags',
        'public_notes',
        'admin_notes',
        'user',
        # 'conversation',
    ]
    list_display = [
        'id',
        'name',
        'phone',
        'location',
        'size',
        'event',
        'state',
        'public_notes',
        'admin_notes',
    ]
    list_filter = [
        'event__year',
        'state',
        'size',
        'is_veteran',
        'is_senior',
        'is_disabled',
        'is_dog',
        'created',
        'updated',
    ]
    search_fields = [
        'user__name',
        'user__phone',
        'name',
        'phone',
        'location',
    ]
    list_editable = [
        # 'user',
        # 'bags',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        RecipientMessageInline,
    ]
    ordering = [
        '-created',
    ]
    readonly_fields = [
        # 'latest_message',
        # 'user_url',
    ]

    actions = [
        send_invitations,
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        queryset |= self.model.objects.filter(user__phone=search_term)
        return queryset, may_have_duplicates


@admin.register(Team)
class TeamAdmin(FSMTransitionMixin, ModelAdmin):

    save_on_top = True
    fields = [
        'state',
        'event',
        'name',
        'phone',
        'nickname',
        'size',
        'public_notes',
        'admin_notes',
        'user',
        # 'conversation',
    ]
    list_display = [
        'id',
        'name',
        'phone',
        'size',
        'nickname',
        # 'nickname',
        # 'recipient_sizes',
        'event',
        'state',
        # 'created',
        'public_notes',
        'admin_notes',
        # 'latest_message',
    ]
    list_filter = [
        'event__year',
        'state',
        'size',
        'created',
        'updated',
    ]
    search_fields = [
        'nickname',
        'name',
        'phone',
        'user__name',
        'user__phone',
    ]
    list_editable = [
        # 'state',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        TeamMessageInline,
    ]
    ordering = [
        '-created',
    ]
    readonly_fields = [
        # 'latest_message',
        # 'user_url',
    ]
    actions = [
        send_invitations,
    ]


    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        queryset |= self.model.objects.filter(user__phone=search_term)
        return queryset, may_have_duplicates


@admin.register(Message)
class MessageAdmin(FSMTransitionMixin, ModelAdmin):
    save_on_top = True

    fields = [
        'id',
        'state',
        'body',
        'sid',
        'to_phone',
        'from_phone',
        'direction',
        'recipient',
        'team',
        'user',
        'created',
        'updated',
    ]
    list_display = [
        'id',
        # 'body',
        # 'updated',
        'recipient',
        'team',
        'created',
        'direction',
        'body',
        'state',
    ]
    list_editable = [
        'recipient',
        'team',
    ]
    list_filter = [
        'direction',
        'state',
    ]
    search_fields = [
    ]
    autocomplete_fields = [
        'user',
        'recipient',
        'team',
    ]
    inlines = [
    ]
    ordering = [
        '-created',
    ]
    readonly_fields = [
        'id',
        'created',
        'updated',
    ]
    actions = [
        mark_read,
        send_message,
    ]


@admin.register(Assignment)
class AssignmentAdmin(ModelAdmin):
    # form = AssignmentForm
    save_on_top = True
    fields = [
        'state',
        'event',
        'recipient',
        'team',
        'public_notes',
        'admin_notes',
        # 'conversation',
    ]
    list_display = [
        'id',
        'state',
        'recipient',
        # 'yard__size',
        'team',
        # 'rake__size',
        'event',
    ]
    list_filter = [
        'event__year',
        'state',
        # 'yard__recipient__size',
        # 'rake__team__size',
        # 'team_state',
    ]

    list_editable = [
    ]
    search_fields = [
        'recipient__user__phone',
        'recipient__user__name',
        'team__user__phone',
        'team__user__name',
        'recipient__location',
    ]

    autocomplete_fields = [
        'recipient',
        'team',
        'event',
    ]
    readonly_fields = [
        # 'yard__size',
        # 'rake__size',
    ]

    ordering = (
        'recipient__user__name',
    )

    # def get_changelist_form(self, request, **kwargs):
    #     return AssignmentForm


@admin.register(Event)
class EventAdmin(ModelAdmin):
    save_on_top = True
    fields = [
        'year',
        'state',
        'deadline',
        'date',
        # 'created',
        # 'updated',
    ]
    list_display = [
        'id',
        'year',
        'state',
        'deadline',
        'date',
        'created',
        'updated',
    ]
    list_filter = [
    ]
    inlines = [
        RecipientInline,
        TeamInline,
    ]
    list_editable = [
    ]
    autocomplete_fields = [
    ]
    search_fields = [
        'year',
    ]



@admin.register(User)
class UserAdmin(UserAdminBase):
    save_on_top = True
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    fieldsets = (
        (None, {
            'fields': [
                'name',
                'phone',
            ]
        }
        ),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_verified',)}),
    )
    list_display = [
        'id',
        'name',
        'phone',
        'created',
        'last_login'
    ]
    list_filter = [
        'is_active',
        'is_admin',
        'is_verified',
        'created',
        'last_login',
    ]
    search_fields = [
        'phone',
        'name',
    ]
    ordering = [
        'phone',
    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': [
                'name',
                'phone',
                'is_admin',
                'is_active',
                'is_verified',
            ]
        }
        ),
    )
    filter_horizontal = ()
    inlines = [
        UserMessageInline,
        TeamInline,
        RecipientInline,
    ]
    readonly_fields = [
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        queryset |= self.model.objects.filter(phone=search_term)
        return queryset, may_have_duplicates


# Use Passwordless for login
admin.site.login = staff_member_required(
    admin.site.login,
    login_url=settings.LOGIN_URL,
)
