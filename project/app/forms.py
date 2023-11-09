# Django
from django import forms
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from phonenumber_field.formfields import PhoneNumberField

# Local
from .models import Recipient
from .models import Team
from .models import User
from .widgets import AddressWidget
from .widgets import CodeWidget


class CallForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = [
            'admin_notes',
            # 'phone',
        ]


class TeamcallForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'admin_notes',
            'actual',
            # 'phone',
        ]


class VerifyCodeForm(forms.Form):
    code = forms.CharField(
        max_length=4,
        required=True,
        help_text='Enter Code',
        widget=CodeWidget(
            attrs={
                'class': 'form-control form-control-lg',
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


class RegisterForm(forms.Form):
    phone = PhoneNumberField(
        required=True,
    )
    name = forms.CharField(
        max_length=40,
        required=True,
        help_text='Your Name',
        widget=forms.TextInput(
            attrs={
                'class': "form-control form-control-lg",
                'placeholder': "Name",
            },
        ),
    )


class RecipientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Overriding required fields in form
        self.fields['name'].required = True
        self.fields['size'].required = True
        self.fields['location'].required = True

    class Meta:
        model = Recipient
        fields = [
            'name',
            'location',
            'size',
            'is_veteran',
            'is_senior',
            'is_disabled',
            'is_dog',
            'notes',
        ]
        labels = {
            "is_dog": "I Have a Dog",
            "is_veteran": "I Am a Veteran",
            "is_senior": "I Am a Senior",
            "is_disabled": "I Am Disabled",
        }
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Anything else we should know? (Optional)',
                    'rows': 5,
                }
            ),
        }
        help_texts = {
        }


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Overriding required fields in form
        self.fields['name'].required = True
        self.fields['size'].required = True

    class Meta:
        model = Team
        fields = [
            'name',
            'size',
            'nickname',
            'reference',
            'notes',
        ]
        labels = {
        }
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Anything else we should know? (Optional)',
                    'rows': 5,
                }
            ),
            'nickname': forms.TextInput(
                attrs={
                    'placeholder': 'Nick Name (optional)',
                }
            ),
            'reference': forms.TextInput(
                attrs={
                    'placeholder': 'Referred by (optional)',
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
