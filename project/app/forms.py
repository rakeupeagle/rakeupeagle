# Django
from django import forms
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

# Local
from .models import Account
from .models import Recipient
from .models import User
from .models import Volunteer
from .widgets import AddressWidget


class AccountAdminForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'id',
            'state',
            'name',
            'email',
            'address',
            'place',
            'is_precise',
            'point',
            'geocode',
            'notes',
            'user',
        ]
        widgets = {
            'address': AddressWidget(
                attrs={'style': "width: 600px;"}
            ),
        }

        help_texts = {
            'name': mark_safe("Please enter your preferred name."),
            'address': mark_safe("Please provide your <strong>residence address</strong>, which will remain <strong>private and confidential</strong> unless we certify."),
            'email': mark_safe("We do not sell, share, or spam you."),
        }



class DeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
    )



class RecipientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Making name required
        self.fields['address'].required = True

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
            'reference',
            'notes',
        ]
        widgets = {
            'reference': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'How did you hear about us? (Optional)',
                    'rows': 1,
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control h-25',
                    'placeholder': 'Anything else we should know? (Optional)',
                    'rows': 5,
                }
            ),
            'address': AddressWidget(),
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
