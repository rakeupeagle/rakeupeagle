# Django
# First-Party
from address.forms import AddressWidget
from address.models import AddressField
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.utils.safestring import mark_safe
from reversion.admin import VersionAdmin

# Local
from .forms import AccountAdminForm
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import VolunteerInline
from .models import Account
from .models import Event
from .models import Picture
from .models import Recipient
from .models import User
from .models import Volunteer


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


@admin.register(Account)
class AccountAdmin(VersionAdmin):
    form = AccountAdminForm
    save_on_top = True
    fields = [
        'state',
        'name',
        'email',
        # 'picture',
        'address',
        # 'user',
        # 'is_steering',
        'notes',
    ]
    list_display = [
        'name',
        'email',
        'address',
        # 'is_public',
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
    save_on_top = True
    fields = [
        'name',
        'phone',
        'email',
        'address',
        'size',
        'is_dog',
        'is_verified',
        'is_waiver',
        'notes',
        'bags',
        'hours',
        'adults',
        'children',
    ]
    list_display = [
        'name',
        'phone',
        'email',
        'address',
        'size',
        'is_dog',
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
        'name',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        VolunteerInline,
    ]
    ordering = [
        'last_name',
        'first_name',
    ]
    readonly_fields = [
        # 'total',
        # 'reps',
    ]
    formfield_overrides = {
        AddressField: {
            'widget': AddressWidget(
                attrs={
                    'style': 'width: 300px;'
                }
            )
        }
    }


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'phone',
        'email',
        'size',
        'notes',
        'user',
        'assignment',
    ]
    list_display = [
        'name',
        'phone',
        'email',
        'size',
        'user',
        'assignment',
    ]
    list_filter = [
        'created',
        'updated',
    ]
    search_fields = [
        'name',
    ]
    list_editable = [
        'assignment',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
    ]
    ordering = [
        'last_name',
        'first_name',
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
