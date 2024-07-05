from django import forms
from django.forms.widgets import DateInput, TextInput

from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__ # type: ignore
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower() # type: ignore
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password','profile_pic', 'address' ]


class ProjectEngineerForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(ProjectEngineerForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = ProjectEngineer
        fields = CustomUserForm.Meta.fields + \
            ['track']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class ManagerForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(ManagerForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Manager
        fields = CustomUserForm.Meta.fields + \
            ['track' ]


class TrackForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(TrackForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Track


class TaskForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Task
        fields = ['name', 'manager', 'track']


class LeaveReportManagerForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportManagerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportManager
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackManagerForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackManagerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackManager
        fields = ['feedback']


class LeaveReportProjectEngineerForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportProjectEngineerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportProjectEngineer
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackProjectEngineerForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackProjectEngineerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackProjectEngineer
        fields = ['feedback']


class ProjectEngineerEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(ProjectEngineerEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = ProjectEngineer
        fields = CustomUserForm.Meta.fields 


class ManagerEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(ManagerEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Manager
        fields = CustomUserForm.Meta.fields


class EditResultForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(EditResultForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ProjectEngineerResult
        fields = ['task', 'projectEngineer', 'weekly', 'monthly']
