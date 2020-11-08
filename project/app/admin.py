# # Django
# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
# from django.urls import reverse
from django.utils.safestring import mark_safe

# Local
from .filters import IsAssignedFilter
# # Local
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import AssignmentInline
from .models import Assignment
from .models import Recipient
from .models import User
from .models import Volunteer


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'phone',
        'email',
        'number',
        'adults',
        'children',
        'is_assigned',
        'notes',
    ]
    list_display = [
        'name',
        'phone',
        'email',
        'number',
        'adults',
        'children',
        'is_assigned',
    ]
    list_filter = [
        'created',
        'updated',
        IsAssignedFilter,
    ]
    search_fields = [
        'name',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        AssignmentInline,
    ]
    ordering = [
        'number',
        'name',
    ]
    readonly_fields = [
        'is_assigned',
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
        'is_assigned',
        'notes',
    ]
    list_display = [
        'name',
        'phone',
        'email',
        'address',
        'size',
        'is_dog',
        # 'is_verified',
        # 'is_waiver',
        # 'created',
        # 'updated',
        'is_assigned',
    ]
    # list_editable = [
    #     'phone',
    #     'email',
    #     'address',
    # ]
    list_filter = [
        'size',
        'is_dog',
        IsAssignedFilter,
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
        AssignmentInline,
    ]
    ordering = [
        'size',
        'name',
    ]
    readonly_fields = [
        'is_assigned',
    ]


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'recipient',
        'volunteer',
        'notes',
    ]
    list_display = [
        'status',
        'recipient',
        'volunteer',
    ]
    list_editable = [
        'recipient',
        'volunteer',
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
                'email',
                'username',
            ]
        }
        ),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    list_display = [
        'name',
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
        'name',
        'email',
        'username',
    ]
    ordering = [
        '-created',
    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': [
                'name',
                'email',
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

    def email_link(self, obj):
        return mark_safe(
            '<a href="mailto:{0}">{0}</a>'.format(
                obj.email,
            )
        )
    email_link.short_description = 'email'
