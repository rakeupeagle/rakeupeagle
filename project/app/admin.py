# Django
# First-Party
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from fsm_admin.mixins import FSMTransitionMixin
from reversion.admin import VersionAdmin

# Local
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import AssignmentInline
from .inlines import MessageInline
from .inlines import RakeInline
from .inlines import YardInline
# from .inlines import RecipientInline
# from .inlines import TeamInline
from .models import Assignment
from .models import Event
from .models import Message
from .models import Picture
from .models import Rake
from .models import Recipient
from .models import Team
from .models import User
from .models import Yard


@admin.register(Recipient)
class RecipientAdmin(VersionAdmin):
    # def team_sizes(self, obj):
    #     lst = [Team.SIZE[x.team.size] for x in obj.assignments.all()]
    #     return "; ".join(
    #         list(lst)
    #     )

    # def latest_message(self, obj):
    #     latest_message = obj.user.messages.filter(
    #         direction=Message.DIRECTION.inbound,
    #     ).latest('created').body
    #     return latest_message

    # # def user_url(self, obj):
    # #     user_url = reverse('admin:app_user_change', args=[obj.user.id])
    # #     return format_html("<a href='{url}'>User</a>", url=user_url)


    save_on_top = True
    fields = [
        'state',
        'name',
        # 'user_url',
        'phone',
        'location',
        'size',
        'is_veteran',
        'is_senior',
        'is_disabled',
        'is_dog',
        'user',
        'public_notes',
        'admin_notes',
        'bags',
    ]
    list_display = [
        'name',
        'phone',
        'user',
        'location',
        # 'user_url',
        # 'is_senior',
        # 'is_disabled',
        # 'is_veteran',
        # 'phone',
        # 'location',
        'size',
        # 'is_dog',
        # 'team_sizes',
        'state',
        # 'created',
        # 'user',
        # 'public_notes',
        # 'admin_notes',
        # 'latest_message',
    ]
    list_filter = [
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
        'name',
        'location',
    ]
    list_editable = [
        'state',
        'phone',
        'user',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        # AssignmentInline,
        YardInline,
    ]
    ordering = [
        'name',
        'created',
    ]
    readonly_fields = [
        # 'latest_message',
        # 'user_url',
    ]


@admin.register(Yard)
class YardAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'state',
        'recipient',
        'public_notes',
        'admin_notes',
        'event',
    ]
    list_display = [
        'state',
        'recipient',
        'public_notes',
        'admin_notes',
        'event',
    ]
    list_filter = [
        'event__year',
        'state',
        'recipient__size',
    ]
    search_fields = [
        'recipient__name',
    ]
    list_editable = [
    ]
    autocomplete_fields = [
        'recipient',
        'event',
    ]
    inlines = [
        AssignmentInline,
    ]
    ordering = [
        'recipient__name',
    ]
    readonly_fields = [
    ]


@admin.register(Rake)
class RakeAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'state',
        'team',
        'public_notes',
        'admin_notes',
        'event',
    ]
    list_display = [
        'state',
        'team',
        'public_notes',
        'admin_notes',
        'event',
    ]
    list_filter = [
        'event__year',
        'state',
        'team__size',
    ]
    search_fields = [
        'team__name',
    ]
    list_editable = [
    ]
    autocomplete_fields = [
        'team',
        'event',
    ]
    inlines = [
        AssignmentInline,
    ]
    ordering = [
        'team__name',
    ]
    readonly_fields = [
    ]


@admin.register(Team)
class TeamAdmin(VersionAdmin):
    # def recipient_sizes(self, obj):
    #     lst = [Recipient.SIZE[x.recipient.size] for x in obj.assignments.all()]

    #     return "; ".join(
    #         list(lst)
    #     )

    # def latest_message(self, obj):
    #     latest_message = obj.user.messages.filter(
    #         direction=Message.DIRECTION.inbound,
    #     ).latest('created').body
    #     return latest_message

    # def user_url(self, obj):
    #     user_url = reverse('admin:app_user_change', args=[obj.user.id])
    #     return format_html("<a href='{url}'>User</a>", url=user_url)

    save_on_top = True
    fields = [
        'state',
        'name',
        # 'user_url',
        'phone',
        'nickname',
        'size',
        'public_notes',
        'admin_notes',
        'user',
    ]
    list_display = [
        'name',
        'nickname',
        'phone',
        'user',
        'size',
        # 'nickname',
        # 'recipient_sizes',
        'state',
        # 'created',
        # 'public_notes',
        # 'admin_notes',
        # 'latest_message',
    ]
    list_filter = [
        'state',
        'size',
        'created',
        'updated',
    ]
    search_fields = [
        'nickname',
        'name',
        'user__phone',
    ]
    list_editable = [
        'state',
        'phone',
        'user',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        # AssignmentInline,
        RakeInline,
    ]
    ordering = [
        'name',
    ]
    readonly_fields = [
        # 'latest_message',
        # 'user_url',
    ]


@admin.register(Assignment)
class AssignmentAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'state',
        'event',
        'yard',
        'rake',
        'public_notes',
        'admin_notes',
    ]
    list_display = [
        'id',
        'state',
        'yard',
        # 'yard__size',
        'rake',
        # 'rake__size',
        'event',
    ]
    list_filter = [
        'event__year',
        'state',
        'yard__recipient__size',
        'rake__team__size',
        # 'team_state',
    ]

    list_editable = [
        'yard',
        'rake',
    ]
    autocomplete_fields = [
        'yard',
        'rake',
        'event',
    ]
    readonly_fields = [
        # 'yard__size',
        # 'rake__size',
    ]


@admin.register(Event)
class EventAdmin(VersionAdmin):
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
        AssignmentInline,
    ]
    list_editable = [
    ]
    autocomplete_fields = [
    ]
    search_fields = [
        'year',
    ]


@admin.register(Message)
class MessageAdmin(VersionAdmin):

    # def user_url(self, obj):
    #     user_url = reverse('admin:app_user_change', args=[obj.user.id])
    #     return format_html("<a href='{url}'>User</a>", url=user_url)

    fields = [
        'id',
        'state',
        'body',
        'sid',
        'to_phone',
        'from_phone',
        'direction',
        'raw',
        'created',
        'updated',
    ]
    list_display = [
        'id',
        # 'user_url',
        'body',
        'direction',
        'created',
        'updated',
    ]
    list_editable = [
    ]
    list_filter = [
        'direction',
        'state',
    ]
    search_fields = [
    ]
    autocomplete_fields = [
    ]
    inlines = [
    ]
    ordering = [
        '-created',
    ]
    readonly_fields = [
        'id',
        'sid',
        # 'to_phone',
        'from_phone',
        'user_id',
        # 'direction',
        'created',
        'updated',
        'raw',
    ]


@admin.register(Picture)
class PictureAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'image',
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
                'is_admin',
                'is_active',
                'is_verified',
            ]
        }
        ),
    )
    filter_horizontal = ()
    inlines = [
        # MessageInline,
    ]
    readonly_fields = [
    ]


# Use Passwordless for login
admin.site.login = staff_member_required(
    admin.site.login,
    login_url=settings.LOGIN_URL,
)
