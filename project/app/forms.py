# # Django
# # Third-Party
# from dal import autocomplete

from django import forms
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase

# # Local
# from .models import Ask
# from .models import Classmate
# from .models import Homeroom
# from .models import Parent
# from .models import School
# from .models import Student
# from .models import Teacher
from .models import User

# from django.core.exceptions import ValidationError
# from django.forms.models import inlineformset_factory


# StudentFormSet = inlineformset_factory(
#     Parent,
#     Student,
#     fields=[
#         'name',
#         'gender',
#         'grade',
#         'school',
#         'parent',
#     ],
#     widgets={
#         'school': autocomplete.ModelSelect2(
#             url='school-autocomplete',
#             attrs={
#                 'data-container-css-class': '',
#                 'data-close-on-select': 'true',
#                 'data-scroll-after-select': 'true',
#                 'data-placeholder': 'Start typing to search....',
#                 'data-minimum-input-length': 3,
#             },
#         ),
#     },
#     extra=1,
#     can_delete=True,
# )


# class SchoolForm(forms.ModelForm):

#     class Meta:
#         model = School
#         fields = [
#             'name',
#             'status',
#             'level',
#             'nces_id',
#             'low_grade',
#             'high_grade',
#             'address',
#             'city',
#             'state',
#             'zipcode',
#             'county',
#             'phone',
#             'website',
#             'lat',
#             'lon',
#         ]


# class ClassmateForm(forms.ModelForm):

#     class Meta:
#         model = Classmate

#         fields = [
#             'from_student',
#             'to_student',
#             'message',
#         ]

#     to_student = forms.ModelChoiceField(
#         queryset=Student.objects.all(),
#         widget=autocomplete.ModelSelect2(
#             url='student-autocomplete',
#             attrs={
#                 'data-container-css-class': ' ',
#                 'data-close-on-select': 'true',
#                 'data-scroll-after-select': 'true',
#                 'data-placeholder': 'Search for students by name, parent name, school name and/or grade...',
#                 'data-minimum-input-length': 3,
#                 'data-html': 'true',
#                 'data-allow-clear': 'true',
#             },
#         ),
#     )
#     message = forms.CharField(
#         required=False,
#         widget=forms.Textarea(
#             attrs={
#                 'class': 'form-control h-25',
#                 'placeholder': 'Personal message (optional)',
#                 'rows': 5,
#             }
#         )
#     )

#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['from_student'].queryset = Student.objects.filter(parent=parent)


# class BuildClassmateForm(forms.Form):

#     student_name = forms.CharField(
#         required=True,
#     )

#     def clean_student_name(self):
#         data = self.cleaned_data['student_name']
#         return data.title()

#     parent_name = forms.CharField(
#         required=True,
#     )

#     def clean_parent_name(self):
#         data = self.cleaned_data['parent_name']
#         return data.title()

#     parent_email = forms.EmailField(
#         required=True,
#         widget=forms.EmailInput(attrs={'class': 'form-control'})
#     )

#     def clean_parent_email(self):
#         data = self.cleaned_data['parent_email']
#         return data.lower()

#     school = forms.ModelChoiceField(
#         queryset=School.objects.all(),
#         # required=True,
#         widget=autocomplete.ModelSelect2(
#             url='school-autocomplete',
#             attrs={
#                 'data-container-css-class': '',
#                 'data-close-on-select': 'true',
#                 'data-scroll-after-select': 'true',
#                 'data-placeholder': 'Add Student School',
#                 'data-minimum-input-length': 3,
#             },
#         ),
#     )
#     grade = forms.ChoiceField(
#         choices=Student.GRADE,
#         required=True,
#     )


# class TeacherForm(forms.ModelForm):

#     school = forms.ModelChoiceField(
#         queryset=School.objects.all(),
#         widget=autocomplete.ModelSelect2(
#             url='school-autocomplete',
#             attrs={
#                 'data-container-css-class': '',
#                 'data-close-on-select': 'true',
#                 'data-scroll-after-select': 'true',
#                 'data-placeholder': 'Nearby School',
#                 'data-minimum-input-length': 3,
#             },
#         ),
#         help_text="Pick a school near where you'd like to teach (doesn't have to be your own school; this is just for location.)",
#     )

#     class Meta:
#         model = Teacher
#         fields = [
#             'is_credential',
#             'levels',
#             'subjects',
#             'school',
#             'rate',
#             'notes',
#         ]
#         labels = {
#             "is_credential": "Credentialed?",
#             "levels": "School Level",
#             "subjects": "School Subjects",
#             "rate": "Hourly Rate Range",
#         }
#         help_texts = {
#             "is_credential": "If you are credentialed please check the box.",
#         }


# class HomeroomForm(forms.ModelForm):

#     class Meta:
#         model = Homeroom
#         fields = [
#             'kind',
#             'schedule',
#             'frequency',
#             'safety',
#             'notes',
#             'goal',
#         ]
#         widgets = {
#             'notes': forms.Textarea(
#                 attrs={
#                     'class': 'form-control h-25',
#                     'placeholder': 'Add other notes about your Homeroom.',
#                     'rows': 5,
#                 }
#             )
#         }
#         help_texts = {
#             'kind': "Choose 'Public' if you'd like others to be able to find and ask to join your Homeroom.<br>  Choose 'Private' if you'd like your Homeroom to be hidden and joinable by invite-only.",
#             'goal': "Choose 'Instruction' if you're seeking a dedicated teacher for your Homeroom.<br>  Choose 'Social' if you're primarily using your school's distance learning material and mainly want social support."
#         }


# class StudentForm(forms.ModelForm):
#     school = forms.ModelChoiceField(
#         queryset=School.objects.all(),
#         widget=autocomplete.ModelSelect2(
#             url='school-autocomplete',
#             attrs={
#                 'data-container-css-class': '',
#                 'data-close-on-select': 'true',
#                 'data-scroll-after-select': 'false',
#                 'data-placeholder': 'Search Schools',
#                 'data-minimum-input-length': 3,
#             },
#         ),
#         help_text="Please select the school your student would be entering in the Fall.",
#     )
#     class Meta:
#         model = Student
#         fields = [
#             'name',
#             'gender',
#             'school',
#             'grade',
#         ]


# class ParentForm(forms.ModelForm):
#     class Meta:
#         model = Parent
#         fields = [
#             'name',
#             'email',
#             'phone',
#             'is_host',
#             'schedule',
#             'frequency',
#             'safety',
#             'notes',
#         ]
#         widgets = {
#             'notes': forms.Textarea(
#                 attrs={
#                     'class': 'form-control h-25',
#                     'placeholder': 'Anything else to share?',
#                     'rows': 5,
#                 }
#             )
#         }
#         labels = {
#             'is_host': "Are you able to host instruction at your house?",
#         }
#         help_texts = {
#             'schedule': "What time of day would you like your homeroom pod to meet?",
#             'frequency': "How many days a week would you like your homeroom pod to meet?",
#             'safety': "Standard safety is rigorous hygiene; <br>Enhanced adds Masks and Distance requirements.",
#         }


# class DeleteForm(forms.Form):
#     confirm = forms.BooleanField(
#         required=True,
#     )


# class SignupForm(forms.Form):
#     name = forms.CharField(
#         required=True,
#         help_text="""Real name strongly encouraged.  However, if necessary use a descriptor like 'Concerned Parent' or 'Father of Two'. (Required)""",
#     )
#     email = forms.EmailField(
#         required=True,
#         help_text="""Your email is private and not shared.  It's used to manage preferences and send adminstrative updates. (Required)""",
#     )
#     password = forms.CharField(
#         required=True,
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         help_text="""A password is necessary to manage preferences. (Required)""",
#     )
#     message = forms.CharField(
#         required=False,
#         help_text="""Please keep your message civil.  I won't post messages that are vulgar, profane, or otherwise inappropriate. (Optional)""",
#         widget=forms.Textarea(
#             attrs={
#                 'class': 'form-control h-25',
#                 'placeholder': 'Your Message to your Public Officials',
#                 'rows': 5,
#             }
#         )
#     )
#     def clean_email(self):
#         data = self.cleaned_data['email']
#         return data.lower()

#     def clean_name(self):
#         data = self.cleaned_data['name']
#         return data.title()


# class AskForm(forms.ModelForm):
#     school = forms.ModelChoiceField(
#         queryset=School.objects.all(),
#         widget=autocomplete.ModelSelect2(
#             url='school-autocomplete',
#             attrs={
#                 'data-container-css-class': '',
#                 'data-close-on-select': 'true',
#                 'data-scroll-after-select': 'false',
#                 'data-placeholder': 'Search Schools',
#                 'data-minimum-input-length': 3,
#             },
#         ),
#         help_text="Please select the school your student would be entering in the Fall.",
#     )

#     class Meta:
#         model = Ask
#         fields = [
#             'student_name',
#             'message',
#             'gender',
#             'school',
#             'grade',
#         ]
#         widgets = {
#             'message': forms.Textarea(
#                 attrs={
#                     'class': 'form-control h-25',
#                     'placeholder': 'You can include a short message with your request.',
#                     'rows': 5,
#                 }
#             )
#         }


# class UserAskForm(forms.ModelForm):

#     class Meta:
#         model = Ask
#         fields = [
#             'student',
#             'message',
#         ]
#         widgets = {
#             'message': forms.Textarea(
#                 attrs={
#                     'class': 'form-control h-25',
#                     'placeholder': 'You can include a short message with your request.',
#                     'rows': 5,
#                 }
#             )
#         }

#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['student'].queryset = Student.objects.filter(parent=parent)


# class AddAskForm(forms.ModelForm):

#     class Meta:
#         model = Ask
#         fields = [
#             'student_name',
#             'parent_name',
#             'parent_email',
#             'message',
#         ]
#         widgets = {
#             'message': forms.Textarea(
#                 attrs={
#                     'class': 'form-control h-25',
#                     'placeholder': 'You can include a short message with your request.',
#                     'rows': 5,
#                 }
#             )
#         }


# class SubscribeForm(forms.Form):
#     email = forms.EmailField(
#         required=True,
#         widget=forms.EmailInput(attrs={'class': 'form-control'})
#     )
#     def clean_email(self):
#         data = self.cleaned_data['email']
#         return data.lower()


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
