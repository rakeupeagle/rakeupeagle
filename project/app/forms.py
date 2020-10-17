# # Django
# # Third-Party
# from dal import autocomplete

# Django
from django import forms
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.core.exceptions import ValidationError

# Local
# # Local
from .models import Recipient
from .models import User
from .models import Volunteer

# from django.forms.models import inlineformset_factory


class VolunteerForm(forms.ModelForm):

    class Meta:
        model = Volunteer
        fields = [
            'name',
            'phone',
            'email',
            'number',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Anything else we should know? (Optional).',
                    'rows': 5,
                }
            )
        }
        help_texts = {
        }



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
            'is_verified',
            'is_waiver',
            'notes',
        ]
        labels = {
            "is_dog": "I Have a Dog",
            "is_verified": "I Am 65+, a Veteran, or Disabled",
            "is_waiver": "I Agree to the Waiver",
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

    def clean_is_waiver(self):
        data = self.cleaned_data['is_waiver']
        if not data:
            raise ValidationError("You must accept the waiver to participate.")
        return data

    def clean_is_verified(self):
        data = self.cleaned_data['is_verified']
        if not data:
            raise ValidationError("You must be over 65, a veteran or disabled to participate.")
        return data




class UserCreationForm(UserCreationFormBase):
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

    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()

    def clean_name(self):
        data = self.cleaned_data['name']
        return data.title()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'name',
        ]


class UserChangeForm(UserChangeFormBase):

    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()

    def clean_name(self):
        data = self.cleaned_data['name']
        return data.title()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'name',
        ]
