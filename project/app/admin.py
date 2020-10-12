# # Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

# # Local
from .forms import UserChangeForm
from .forms import UserCreationForm
# from .inlines import HomeroomInline
# from .inlines import StudentInline
# from .models import Account
# from .models import Ask
# from .models import Classmate
# from .models import Homeroom
# from .models import Parent
# from .models import School
# from .models import Student
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
        'number',
        'notes',
    ]
    list_display = [
        'name',
        'phone',
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
    ]


# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     save_on_top = True
#     fields = [
#         'user',
#         'is_credential',
#         'levels',
#         'subjects',
#         'school',
#         'notes',
#     ]
#     list_display = [
#         'user',
#         'created',
#         'updated',
#     ]
#     list_filter = [
#         'is_credential',
#         'levels',
#         'subjects',
#         # 'school',
#         'created',
#         'updated',
#     ]
#     search_fields = [
#         'user__name',
#     ]
#     autocomplete_fields = [
#         'user',
#         'school',
#     ]
#     inlines = [
#         # StudentInline,
#     ]


# @admin.register(School)
# class SchoolAdmin(admin.ModelAdmin):
#     fields = [
#         'name',
#         'status',
#         'level',
#         'nces_id',
#         'grades',
#         'low_grade',
#         'high_grade',
#         'address',
#         'city',
#         'state',
#         'zipcode',
#         'county',
#         'phone',
#         'website',
#         'lat',
#         'lon',
#     ]
#     list_display = [
#         'name',
#         'level',
#         'nces_id',
#         'low_grade',
#         'high_grade',
#         'city',
#         'state',
#         'phone',
#         'website',
#         'lat',
#         'lon',
#         'created',
#         'updated',
#     ]
#     list_filter = [
#         'level',
#         'status',
#     ]
#     search_fields = [
#         'name',
#         'nces_id',
#     ]
#     inlines = [
#         # StudentInline,
#     ]
#     autocomplete_fields = [
#     ]


# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = [
#         'parent',
#         'school',
#         'grade',
#     ]
#     list_filter = [
#         'grade',
#         'created',
#         'updated',
#     ]
#     search_fields = [
#         'name',
#         'parent__user__name',
#     ]
#     inlines = [
#     ]
#     autocomplete_fields = [
#         'parent',
#         'school',
#     ]


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
