# Django
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from phonenumber_field.formfields import PhoneNumberField

# Local
from .models import Assignment
from .models import Message
from .models import Recipient
from .models import Team
from .models import User
from .widgets import CodeWidget


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            'id',
            'state',
            'recipient',
            'team',
            'event',
        ]

        # widgets = {
        #     'yard': AutocompleteSelect(
        #         Assignment._meta.get_field('yard').remote_field,
        #         admin.site,
        #         attrs={
        #             'data-dropdown-auto-width': 'true',
        #             'style': "width: 100%;",
        #         }
        #     ),
        #     'rake': AutocompleteSelect(
        #         Assignment._meta.get_field('rake').remote_field,
        #         admin.site,
        #         attrs={
        #             'data-dropdown-auto-width': 'true',
        #             'style': "width: 100%;",
        #         }
        #     ),
        # }


# class CallForm(forms.ModelForm):
#     class Meta:
#         model = Recipient
#         fields = [
#             'notes',
#             # 'phone',
#         ]


# class TeamcallForm(forms.ModelForm):
#     class Meta:
#         model = Team
#         fields = [
#             'notes',
#             'adults',
#             # 'phone',
#         ]


class VerifyCodeForm(forms.Form):
    code = forms.CharField(
        max_length=4,
        required=True,
        help_text='Enter Code',
        widget=CodeWidget(
            attrs={
                'class': 'form-control form-control-lg',
                'autocomplete': 'off',
            }
        )
    )


class DeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
    )


class LoginForm(forms.Form):
    phone = PhoneNumberField(
        required=True,
    )


class AccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'phone',
            'name',
        ]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'body',
        ]


class RecipientForm(forms.ModelForm):
    comments = forms.CharField(
        max_length=1024,
    )

    class Meta:
        model = Recipient
        fields = [
            'phone',
            'name',
            'location',
            'size',
            'is_veteran',
            'is_senior',
            'is_disabled',
            'place_id',
            'point',
            'comments',
        ]
        labels = {
            # "is_dog": "I Have a Dog",
            "is_veteran": "I Am a Veteran",
            "is_senior": "I Am a Senior",
            "is_disabled": "I Am Disabled",
        }
        widgets = {
            'size': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg',
                }
            ),
        }
        help_texts = {
            # "is_dog": "I Have a Dog",
            "is_veteran": "I Am a Veteran",
            "is_senior": "I Am a Senior",
            "is_disabled": "I Am Disabled",
        }


class TeamForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Overriding required fields in form
    #     self.fields['name'].required = True
    #     self.fields['size'].required = True

    comments = forms.CharField(
        max_length=1024,
    )

    class Meta:
        model = Team
        fields = [
            'phone',
            'name',
            'size',
            'nickname',
            'comments',
        ]
        labels = {
        }
        widgets = {
            'size': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg',
                }
            ),
            'nickname': forms.TextInput(
                attrs={
                    'placeholder': 'Nick Name (optional)',
                }
            ),
        }
        help_texts = {
        }


class UserCreationForm(UserCreationFormBase):
    """
    Custom user creation form
    """

    # Bypass password requirement
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'phone',
            'name',
        ]


class UserChangeForm(UserChangeFormBase):
    """
    Custom user change form
    """

    class Meta:
        model = User
        fields = [
            'phone',
            'name',
        ]
