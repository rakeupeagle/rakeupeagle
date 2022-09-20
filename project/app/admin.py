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
from leaflet.admin import LeafletGeoAdminMixin
from leaflet_admin_list.admin import LeafletAdminListMixin
from polymorphic.admin import PolymorphicChildModelAdmin
from polymorphic.admin import PolymorphicParentModelAdmin
from reversion.admin import VersionAdmin

# Local
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import AssignmentInline
from .inlines import MessageInline
# from .inlines import RecipientInline
# from .inlines import TeamInline
from .models import Account
from .models import Assignment
from .models import Message
from .models import Picture
from .models import Recipient
from .models import Team
from .models import Topic
from .models import User


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


@admin.register(Picture)
class PictureAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'image',
    ]

# @admin.register(Topic)
# class TopicAdmin(VersionAdmin):
#     save_on_top = True
#     fields = [
#     ]
#     list_filter = [
#     ]


@admin.register(Account)
class AccountAdmin(PolymorphicParentModelAdmin):
    save_on_top = True
    fields = [
        'name',
        'phone',
    ]
    child_models = [
        Recipient,
        Team,
    ]
    list_filter = [
    ]
    search_fields = [
        'name',
        'phone',
    ]

@admin.register(Recipient)
class RecipientAdmin(PolymorphicChildModelAdmin):

    # def get_geojson_properties(self, request, name, o, queryset):
    #     '''returns a `properties` member of the GeoJSON `Feature` instance representing the instance `o` geometry field `name`'''
    #     r = {
    #         'field': name,
    #         'app_label': o._meta.app_label,
    #         'model_name': o._meta.model_name,
    #         'pk': str(o.pk),
    #     }
    #     popup = self.get_geojson_feature_popup(request, name, o, queryset)
    #     tooltip = self.get_geojson_feature_tooltip(request, name, o, queryset)
    #     point_style = self.get_geojson_feature_point_style(request, name, o, queryset)
    #     line_style = self.get_geojson_feature_line_style(request, name, o, queryset)
    #     if popup:
    #         r['popup'] = popup
    #     if tooltip:
    #         r['tooltip'] = tooltip

    #     if point_style:
    #         r['point_style'] = point_style
    #     if line_style:
    #         r['line_style'] = line_style
    #     return r


    # def team_sizes(self, obj):
    #     lst = [Team.SIZE[x.team.size] for x in obj.assignments.all()]

    #     return "; ".join(
    #         list(lst)
    #     )

    # def click_phone(self, obj):
    #     return format_html('<a href="tel://{}">{}</a>', obj.phone, obj.phone.as_national)

    # click_phone.short_description = "Phone"



    save_on_top = True
    fields = [
        'state',
        'name',
        'phone',
        'location',
        'size',
        'is_dog',
        'user',
        # 'click_phone',
        # 'is_verified',
        # 'is_waiver',
        'notes',
        'admin_notes',
        # 'bags',
        # 'hours',
    ]
    list_display = [
        'name',
        'phone',
        'location',
        'size',
        'is_dog',
        # 'team_sizes',
        'state',
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
        'state',
        'size',
        'is_dog',
        'created',
        'updated',
    ]
    search_fields = [
        # 'user__name',
        # 'user__phone',
        'location',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        # AssignmentInline,
    ]
    ordering = [
        'created',
    ]
    readonly_fields = [
        # 'click_phone',
        'user',
        'notes',
        # 'reps',
    ]


@admin.register(Topic)
class TopicAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'name',
        'body',
    ]
    list_display = [
        'name',
    ]
    list_editable = [
    ]
    list_filter = [
    ]
    search_fields = [
        'name',
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


@admin.register(Team)
class TeamAdmin(PolymorphicChildModelAdmin):
    # def recipient_sizes(self, obj):
    #     lst = [Recipient.SIZE[x.recipient.size] for x in obj.assignments.all()]

    #     return "; ".join(
    #         list(lst)
    #     )

    save_on_top = True
    fields = [
        'state',
        'nickname',
        'name',
        'phone',
        'size',
        'actual',
        'reference',
        'notes',
        'admin_notes',
        'user',
    ]
    list_display = [
        'nickname',
        'name',
        'phone',
        'size',
        # 'recipient_sizes',
        'state',
    ]
    list_filter = [
        'state',
        'size',
        'created',
        'updated',
    ]
    search_fields = [
        # 'user__name',
        # 'user__id',
        'nickname',
        'name',
    ]
    list_editable = [
    ]
    autocomplete_fields = [
        # 'user',
    ]
    inlines = [
        # AssignmentInline,
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
                'phone',
                'name',
            ]
        }
        ),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    list_display = [
        'username',
        'phone',
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
    ]
    readonly_fields = [
        'username',
    ]

# Use Auth0 for login
admin.site.login = staff_member_required(
    admin.site.login,
    login_url=settings.LOGIN_URL,
)
