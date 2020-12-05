# Django
# First-Party
from address.forms import AddressWidget
from address.models import AddressField
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.utils.safestring import mark_safe

# Local
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import VolunteerInline
from .models import Picture
from .models import Recipient
from .models import User
from .models import Volunteer


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
        'total',
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
        'total',
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
        'number',
        'notes',
        'recipient',
    ]
    list_display = [
        'name',
        'phone',
        'email',
        'number',
        'recipient',
    ]
    list_filter = [
        'created',
        'updated',
    ]
    search_fields = [
        'name',
    ]
    list_editable = [
        'number',
        'recipient',
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
