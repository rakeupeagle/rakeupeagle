# Django
from django import forms
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

# Local
from .models import Recipient
from .models import Team
from .models import User
from .widgets import AddressWidget


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


class DeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
    )


class RecipientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Overriding required fields in form
        self.fields['size'].required = True
        self.fields['location'].required = True

    class Meta:
        model = Recipient
        fields = [
            'location',
            'size',
            'is_dog',
            'notes',
        ]
        labels = {
            "is_dog": "I Have a Dog",
        }
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Anything else we should know? (Optional)',
                    'rows': 5,
                }
            ),
            'location': AddressWidget(
                attrs={
                    'placeholder': 'Location Address',
                },
            ),
        }
        help_texts = {
        }


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Overriding required fields in form
        self.fields['size'].required = True

    class Meta:
        model = Team
        fields = [
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
    Custom user creation form for Auth0
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
            'username',
            'phone',
            'name',
        ]


class UserChangeForm(UserChangeFormBase):
    """
    Custom user change form for Auth0
    """

    class Meta:
        model = User
        fields = [
            'username',
            'phone',
            'name',
        ]
