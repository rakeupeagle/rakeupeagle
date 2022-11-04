# Django
# First-Party
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin as UserAdminBase
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


    save_on_top = True
    fields = [
        'state',
        'name',
        'phone',
        'location',
        'size',
        'is_dog',
        'user',
        'notes',
        'admin_notes',
    ]
    list_display = [
        'name',
        'phone',
        'location',
        'size',
        'is_dog',
        'team_sizes',
        'state',
        'created',
        'user',
    ]
    list_filter = [
        'state',
        'size',
        'is_dog',
        'created',
        'updated',
    ]
    search_fields = [
        'name',
        'location',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        AssignmentInline,
    ]
    ordering = [
        'created',
    ]
    readonly_fields = [
    ]


@admin.register(Team)
class TeamAdmin(VersionAdmin):
    def recipient_sizes(self, obj):
        lst = [Recipient.SIZE[x.recipient.size] for x in obj.assignments.all()]

        return "; ".join(
            list(lst)
        )

    save_on_top = True
    fields = [
        'state',
        'name',
        'phone',
        'nickname',
        'size',
        'notes',
        'admin_notes',
        'user',
    ]
    list_display = [
        'name',
        'phone',
        'size',
        'nickname',
        'recipient_sizes',
        'state',
        'created',
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
    ]
    list_editable = [
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        AssignmentInline,
    ]
    ordering = [
    ]
    readonly_fields = [
    ]


@admin.register(Assignment)
class AssignmentAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'recipient',
        'team',
    ]
    list_display = [
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
        # 'direction',
        'created',
        'updated',
        'raw',
    ]

    # def user_link(self, obj):
    #     try:
    #         name = obj.user.name if obj.user.name else 'Unknown'
    #     except AttributeError:
    #         name = 'Unknown'
    #     try:
    #         response = mark_safe('<a href="{}">{}</a>'.format(
    #             reverse("admin:app_user_change", args=(obj.user.pk,)),
    #             name,
    #         ))
    #     except AttributeError:
    #         response = None
    #     return response
    # user_link.short_description = 'user'


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
                'phone',
            ]
        }
        ),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    list_display = [
        'username',
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
