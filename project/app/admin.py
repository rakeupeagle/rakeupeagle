# Django
# First-Party
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.urls import reverse
from django.utils.safestring import mark_safe
from reversion.admin import VersionAdmin

# Local
from .forms import AccountAdminForm
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import AssignmentInline
from .inlines import MessageInline
from .inlines import RecipientInline
from .inlines import VolunteerInline
from .models import Account
from .models import Assignment
from .models import Event
from .models import Message
from .models import Picture
from .models import Recipient
from .models import User
from .models import Volunteer


@admin.register(Assignment)
class AssignmentAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'recipient',
        'volunteer',
    ]
    list_display = [
        'id',
        'recipient',
        'volunteer',
    ]
    list_editable = [
        'recipient',
        'volunteer',
    ]
    autocomplete_fields = [
        'recipient',
        'volunteer',
    ]




@admin.register(Account)
class AccountAdmin(VersionAdmin):
    form = AccountAdminForm
    save_on_top = True
    fields = [
        'state',
        'name',
        'phone',
        # 'picture',
        # 'user',
        # 'is_steering',
        'notes',
    ]
    list_display = [
        'name',
        # 'email',
        'phone',

        # 'is_spouse',
        # 'is_steering',
        # 'zone',
        'state',
        'created',
        'updated',
    ]
    list_editable = [
    ]
    list_filter = [
        'state',
        # 'is_steering',
        # 'is_spouse',
        # 'zone',
        'created',
        'updated',
    ]
    search_fields = [
        'name',
        'email',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        MessageInline,
        RecipientInline,
        VolunteerInline,
    ]
    ordering = [
        '-created',
    ]
    readonly_fields = [
        'created',
    ]


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'image',
    ]


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):

    def volunteer_sizes(self, obj):
        lst = [Volunteer.SIZE[x.volunteer.size] for x in obj.assignments.all()]

        return "; ".join(
            list(lst)
        )

    save_on_top = True
    fields = [
        'size',
        'is_dog',
        # 'is_verified',
        # 'is_waiver',
        'notes',
        'bags',
        'hours',
        'location',
        'account',
    ]
    list_display = [
        'location',
        'size',
        'is_dog',
        'volunteer_sizes',
        # 'notes',
        # 'is_verified',
        # 'is_waiver',
        # 'created',
        # 'total',
    ]
    list_editable = [
        # 'bags',
        # 'hours',
        # 'persons',
    ]
    list_filter = [
        'size',
        'is_dog',
        'created',
        'updated',
    ]
    search_fields = [
        'account__name',
        'account__phone',
    ]
    autocomplete_fields = [
        'account',
    ]
    inlines = [
        AssignmentInline,
    ]
    ordering = [
        'created',
    ]
    readonly_fields = [
        # 'total',
        # 'reps',
    ]


@admin.register(Event)
class EventAdmin(VersionAdmin):
    save_on_top = True
    autocomplete_fields = [
        # 'account',
        # 'voter',
    ]
    fields = [
        'name',
        'state',
        'description',
        'date',
    ]
    list_display = [
        'name',
        'date',
    ]
    list_editable = [
    ]
    list_filter = [
        'date',
        'state',
        # 'is_spouse',
        # 'zone',
    ]
    search_fields = [
    ]


@admin.register(Message)
class MessageAdmin(VersionAdmin):

    fields = [
        'id',
        'state',
        'account',
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
        'account_link',
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
        'account',
    ]
    autocomplete_fields = [
        'account',
    ]
    inlines = [
        # StudentInline,
        # CommentInline,
    ]
    ordering = [
        '-created',
    ]
    readonly_fields = [
        'id',
        'sid',
        'to_phone',
        'from_phone',
        'direction',
        'created',
        'updated',
        'raw',
        'account_link',
    ]

    def account_link(self, obj):
        try:
            name = obj.account.name if obj.account.name else 'Unknown'
        except AttributeError:
            name = 'Unknown'
        try:
            response = mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:app_account_change", args=(obj.account.pk,)),
                name,
            ))
        except AttributeError:
            response = None
        return response
    account_link.short_description = 'account'


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'team',
        'size',
        'reference',
        'notes',
        'account',
    ]
    list_display = [
        'team',
        'size',
        'reference',
        'account',
    ]
    list_filter = [
        'created',
        'updated',
    ]
    search_fields = [
        'account__name',
        'account__id',
    ]
    list_editable = [
    ]
    autocomplete_fields = [
        'account',
    ]
    inlines = [
        AssignmentInline,
    ]
    ordering = [
    ]
    readonly_fields = [
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
            ]
        }
        ),
        ('Data', {
            'fields': [
                'name',
                'email',
            ]
        }
        ),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    list_display = [
        # 'username',
        'name',
        'email',
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
        'name',
        'email',
    ]
    ordering = [
        '-created',
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
    ]
    readonly_fields = [
        'name',
        'email',
    ]

# Use Auth0 for login
admin.site.login = staff_member_required(
    admin.site.login,
    login_url=settings.LOGIN_URL,
)
