# Django
# First-Party
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.gis.admin.options import GISModelAdmin
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from fsm_admin.mixins import FSMTransitionMixin
from reversion.admin import VersionAdmin

# Local
from .forms import AssignmentForm
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import AssignmentInline
from .inlines import ConversationInline
from .inlines import MessageArchiveInline
from .inlines import MessageInline
from .inlines import ParticipantInline
from .inlines import RakeInline
from .inlines import ReceiptInline
from .inlines import YardInline
# from .inlines import RecipientInline
# from .inlines import TeamInline
from .models import Assignment
from .models import Conversation
from .models import Event
from .models import Message
from .models import MessageArchive
from .models import Participant
from .models import Picture
from .models import Rake
from .models import Receipt
from .models import Recipient
from .models import Team
from .models import User
from .models import Yard


class DirectionListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Direction'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "direction"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        values = [
            ('inbound', 'Inbound'),
            ('outbound', 'Outbound'),
        ]

        return values

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'outbound':
            return queryset.filter(
                author__isnull=True,
            )
        elif self.value() == 'inbound':
            return queryset.filter(
                author__isnull=False,
            )



@admin.register(Recipient)
class RecipientAdmin(GISModelAdmin):
    save_on_top = True
    fields = [
        'state',
        'location',
        'address',
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
        'conversation',
    ]
    list_display = [
        'id',
        'user',
        'location',
        'address',
        'size',
        'state',
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
        'user__name',
        'user__phone',
        'location',
    ]
    list_editable = [
        # 'state',
        # 'user',
        'location',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        # AssignmentInline,
        YardInline,
    ]
    ordering = [
        'created',
    ]
    readonly_fields = [
        # 'latest_message',
        # 'user_url',
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        queryset |= self.model.objects.filter(user__phone=search_term)
        return queryset, may_have_duplicates


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
        'id',
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
        'recipient__user__name',
        'recipient__location',
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
        'recipient__user__name',
    ]
    readonly_fields = [
    ]


@admin.register(Rake)
class RakeAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'state',
        'public_notes',
        'admin_notes',
        'team',
        'event',
    ]
    list_display = [
        'id',
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
        'team__nickname',
        'team__user__name',
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
        'team__nickname',
        'team__user__name',
    ]
    readonly_fields = [
    ]


@admin.register(Team)
class TeamAdmin(VersionAdmin):

    save_on_top = True
    fields = [
        'state',
        'nickname',
        'size',
        'public_notes',
        'admin_notes',
        'user',
        'conversation',
    ]
    list_display = [
        'id',
        'nickname',
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
        'user__name',
        'user__phone',
    ]
    list_editable = [
        'state',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        # AssignmentInline,
        RakeInline,
    ]
    ordering = [
    ]
    readonly_fields = [
        # 'latest_message',
        # 'user_url',
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        queryset |= self.model.objects.filter(user__phone=search_term)
        return queryset, may_have_duplicates


@admin.register(Assignment)
class AssignmentAdmin(VersionAdmin):
    # form = AssignmentForm
    save_on_top = True
    fields = [
        'state',
        'event',
        'yard',
        'rake',
        'public_notes',
        'admin_notes',
        'conversation',
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
        # 'yard',
        # 'rake',
    ]
    search_fields = [
        'yard__recipient__user__phone',
        'yard__recipient__user__name',
        'rake__team__user__phone',
        'rake__team__user__name',
        'yard__recipient__location',
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

    ordering = (
        'yard__recipient__user__name',
    )

    def get_changelist_form(self, request, **kwargs):
        return AssignmentForm


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
        AssignmentInline,
    ]
    list_editable = [
    ]
    autocomplete_fields = [
    ]
    search_fields = [
        'year',
    ]


# Twilio
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'sid',
        'state',
        'name',
        'date_created',
        'date_updated',
    ]

    list_display = [
        'id',
        'sid',
        'state',
        'date_created',
        'date_updated',
        # 'timers',
        # 'url',
        # 'links',
        # 'bindings',
        # 'name',
        # 'unique_name',
        # 'attributes',
        # 'origination',
    ]
    ordering = [
    ]
    search_fields = [
        'sid',
    ]
    list_filter = [
        'state',
    ]
    readonly_fields = [
        'sid',
        # 'state',
        'date_created',
        'date_updated',
    ]
    inlines = [
        ParticipantInline,
        MessageInline,
    ]
    list_editable = [
    ]
    autocomplete_fields = [
        # 'user',
    ]


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'sid',
        # 'attributes',
        # 'messaging_binding',
        'last_read_message_index',
        'last_read_timestamp',
        'date_created',
        'date_updated',
        # 'url',
        # 'conversation_sid',
        # 'origination',
        'conversation',
        'phone',
    ]

    list_display = [
        'id',
        'sid',
        # 'messaging_binding',
        'date_created',
        'date_updated',
        'last_read_message_index',
        'last_read_timestamp',
        # 'conversation_sid',
        # 'origination',
        'conversation',
        'phone',
    ]
    ordering = [
    ]
    search_fields = [
        'sid',
    ]
    list_filter = [
    ]
    inlines = [
        # ReceiptInline,
    ]
    list_editable = [
    ]
    readonly_fields = [
        'sid',
        'date_created',
        'date_updated',
        'last_read_message_index',
        'last_read_timestamp',
        'conversation',
    ]
    autocomplete_fields = [
        'conversation',
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    save_on_top = True

    actions = [
        # block_message,
    ]
    fields = [
        'sid',
        'index',
        'author',
        'body',
        'media',
        # 'attributes',
        'date_created',
        'date_updated',
        # 'url',
        # 'delivery',
        # 'links',
        'conversation',
        'content',
    ]

    list_display = [
        'id',
        'body',
        # 'sid',
        'index',
        'author',
        # 'body',
        # 'media',
        # 'attributes',
        # 'delivery',
        # 'date_created',
        # 'date_updated',
        # 'url',
        # 'links',
        'conversation',
        # 'content'
    ]
    ordering = [
    ]
    search_fields = [
        'author',
        'sid',
        'body',
    ]
    list_filter = [
        DirectionListFilter,
        # 'delivery',
    ]
    readonly_fields = [
        'sid',
        'index',
        'date_created',
        'date_updated',
    ]
    inlines = [
        ReceiptInline,
    ]
    list_editable = [
    ]
    autocomplete_fields = [
        'conversation',
        # 'content',
    ]


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'sid',
        'status',
        'error_code',
        'date_created',
        'date_updated',
        'conversation',
        'participant',
        'message',
    ]

    list_display = [
        'id',
        'sid',
        'status',
        'error_code',
        'date_created',
        'date_updated',
        'conversation',
        'participant',
        'message',
    ]
    ordering = [
    ]
    search_fields = [
    ]
    list_filter = [
        'status',
    ]
    inlines = [
    ]
    list_editable = [
    ]
    readonly_fields = [
        'sid',
        'status',
        'error_code',
        'date_created',
        'date_updated',
        'participant',
        'message',
        'conversation',
    ]
    autocomplete_fields = [
        'participant',
        'message',
        'conversation',
    ]


@admin.register(MessageArchive)
class MessageArchiveAdmin(VersionAdmin):

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
                'is_admin',
                'is_active',
                'is_verified',
            ]
        }
        ),
    )
    filter_horizontal = ()
    inlines = [
        # ConversationInline,
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
