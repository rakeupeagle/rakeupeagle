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
# from .inlines import RecipientInline
# from .inlines import TeamInline
from .models import Assignment
from .models import Message
from .models import Picture
from .models import Recipient
from .models import Team
from .models import User


@admin.register(Recipient)
class RecipientAdmin(VersionAdmin):
    def team_sizes(self, obj):
        lst = [Team.SIZE[x.team.size] for x in obj.assignments.all()]
        return "; ".join(
            list(lst)
        )

    def latest_message(self, obj):
        latest_message = obj.user.messages.filter(
            direction=Message.DIRECTION.inbound,
        ).latest('created').body
        return latest_message

    # def user_url(self, obj):
    #     user_url = reverse('admin:app_user_change', args=[obj.user.id])
    #     return format_html("<a href='{url}'>User</a>", url=user_url)


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
        'notes',
        'admin_notes',
        'bags',
    ]
    list_display = [
        'name',
        'phone',
        'location',
        # 'user_url',
        # 'is_senior',
        # 'is_disabled',
        # 'is_veteran',
        # 'phone',
        # 'location',
        'size',
        # 'is_dog',
        'team_sizes',
        'state',
        # 'created',
        # 'user',
        # 'notes',
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
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        AssignmentInline,
    ]
    ordering = [
        'name',
        'created',
    ]
    readonly_fields = [
        # 'latest_message',
        # 'user_url',
    ]


@admin.register(Team)
class TeamAdmin(VersionAdmin):
    def recipient_sizes(self, obj):
        lst = [Recipient.SIZE[x.recipient.size] for x in obj.assignments.all()]

        return "; ".join(
            list(lst)
        )

    def latest_message(self, obj):
        latest_message = obj.user.messages.filter(
            direction=Message.DIRECTION.inbound,
        ).latest('created').body
        return latest_message

    def user_url(self, obj):
        user_url = reverse('admin:app_user_change', args=[obj.user.id])
        return format_html("<a href='{url}'>User</a>", url=user_url)

    save_on_top = True
    fields = [
        'state',
        'name',
        'user_url',
        'phone',
        'nickname',
        'size',
        'notes',
        'admin_notes',
        'user',
    ]
    list_display = [
        'name',
        'user',
        # 'phone',
        'size',
        # 'nickname',
        'recipient_sizes',
        'state',
        # 'created',
        # 'notes',
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
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        AssignmentInline,
    ]
    ordering = [
        'name',
    ]
    readonly_fields = [
        # 'latest_message',
        'user_url',
    ]


@admin.register(Assignment)
class AssignmentAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'recipient',
        'team',
    ]
    list_display = [
        'id',
        'recipient',
        'team',
    ]
    list_filter = [
    ]

    list_editable = [
        # 'recipient',
        # 'team',
    ]
    autocomplete_fields = [
        'recipient',
        'team',
    ]


@admin.register(Message)
class MessageAdmin(VersionAdmin):

    def user_url(self, obj):
        user_url = reverse('admin:app_user_change', args=[obj.user.id])
        return format_html("<a href='{url}'>User</a>", url=user_url)

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
        'user_url',
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
        'to_phone',
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
                'username',
                'name',
                'phone',
            ]
        }
        ),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    list_display = [
        'username',
        'name',
        'phone',
        'created',
        'last_login'
    ]
    list_filter = [
        'is_active',
        'is_admin',
        'created',
        'last_login',
    ]
    search_fields = [
        'username',
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
                'username',
                'is_admin',
                'is_active',
            ]
        }
        ),
    )
    filter_horizontal = ()
    inlines = [
        MessageInline,
    ]
    readonly_fields = [
        'username',
    ]

# Use Auth0 for login
admin.site.login = staff_member_required(
    admin.site.login,
    login_url=settings.LOGIN_URL,
)
