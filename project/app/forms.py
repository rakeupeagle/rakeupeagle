# Django
from django import forms
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.core.exceptions import ValidationError

# Local
from .models import Recipient
from .models import User
from .models import Volunteer


class DeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
    )



class RecipientForm(forms.ModelForm):

    class Meta:
        model = Recipient
        fields = [
            'name',
            'phone',
            'email',
            'address',
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
            )
        }
        help_texts = {
        }


class VolunteerForm(forms.ModelForm):

    class Meta:
        model = Volunteer
        fields = [
            'name',
            'phone',
            'email',
            'size',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Anything else we should know? (Optional)',
                    'rows': 5,
                }
            )
        }
        help_texts = {
            'size': 'The size of your group.  (Children of sufficient age can be combined as a "adult" for the purposes of this question.)',
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
        ]


class UserChangeForm(UserChangeFormBase):
    """
    Custom user change form for Auth0
    """

    class Meta:
        model = User
        fields = [
            'username',
        ]
