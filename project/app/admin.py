# # Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

# # Local
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import AssignmentInline
from .models import Recipient
from .models import User
from .models import Volunteer

# from django.urls import reverse
# from django.utils.safestring import mark_safe



@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'phone',
        'email',
        'number',
        'notes',
    ]
    list_display = [
        'name',
        'phone',
        'email',
        'number',
        'created',
        'updated',
    ]
    list_filter = [
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
    ]
    list_display = [
        'name',
        'phone',
        'email',
        'address',
        'size',
        'is_dog',
        'is_verified',
        'is_waiver',
        'created',
        'updated',
    ]
    list_filter = [
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
                # 'account_link',
                # 'parent_link',
                # 'teacher_link',
            ]
        }
        ),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    list_display = [
        'name',
        # 'email_link',
        # 'parent_link',
        # 'teacher_link',
        'created',
        'last_login'
    ]
    # list_select_related = [
    #     'parent',
    #     'teacher',
    #     'account',
    # ]
    # readonly_fields = [
    #     'account_link',
    #     'parent_link',
    #     'teacher_link',
    # ]
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
        # StudentInline,
    ]

    def email_link(self, obj):
        return mark_safe(
            '<a href="mailto:{0}">{0}</a>'.format(
                obj.email,
            )
        )
    email_link.short_description = 'email'

    # def account_link(self, obj):
    #     return mark_safe(
    #         '<a href="{}">{}</a>'.format(
    #             reverse(
    #                 "admin:app_account_change",
    #                 args=[obj.account.pk,]
    #             ),
    #             'Account',
    #         )
    #     )
    # account_link.short_description = 'account'

    # def parent_link(self, obj):
    #     return mark_safe(
    #         '<a href="{}">{}</a>'.format(
    #             reverse(
    #                 "admin:app_parent_change",
    #                 args=[obj.parent.pk,]
    #             ),
    #             'Parent',
    #         )
    #     )
    # parent_link.short_description = 'parent'

    # def teacher_link(self, obj):
    #     return mark_safe(
    #         '<a href="{}">{}</a>'.format(
    #             reverse(
    #                 "admin:app_teacher_change",
    #                 args=[obj.teacher.pk,]
    #             ),
    #             'Teacher',
    #         )
    #     )
    # teacher_link.short_description = 'teacher'
