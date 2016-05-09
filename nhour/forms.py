from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from nhour.models import RegularEntry, System, Project, Task, SpecialEntry, Activity, Entry


class EntryForm(ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)

    class Meta:
        fields = ['user', 'week', 'year', 'hours', 'comment']
        widgets = {'user': forms.HiddenInput(),
                   'week': forms.HiddenInput(),
                   'year': forms.HiddenInput(),
                   'hours': forms.HiddenInput()}


class RegularEntryForm(EntryForm):
    system = forms.ModelChoiceField(System.objects.all(), empty_label="Select a system")
    project = forms.ModelChoiceField(Project.objects.all(), empty_label="Select a project", required=False)
    task = forms.ModelChoiceField(Task.objects.all(), empty_label="Select a task")
    class Meta(EntryForm.Meta):
        model = RegularEntry
        fields = ['system', 'project', 'task'] + EntryForm.Meta.fields


class SpecialEntryForm(EntryForm):
    activity = forms.ModelChoiceField(Activity.objects.all(), empty_label="Select an activity")
    class Meta(EntryForm.Meta):
        model = SpecialEntry
        fields = ["activity"] + EntryForm.Meta.fields


def entry_form_factory(instance: Entry, *args, **kwargs) -> EntryForm:

    if type(instance) == Entry:
        if hasattr(instance, "regularentry"):
            return RegularEntryForm(instance=instance.regularentry, *args, **kwargs)
        elif hasattr(instance, "specialentry"):
            return SpecialEntryForm(instance=instance.specialentry, *args, **kwargs)

    elif type(instance) == SpecialEntry:
        return SpecialEntryForm(instance=instance, *args, **kwargs)
    else:
        return RegularEntryForm(instance=instance, *args, **kwargs)

class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password])
    password_again = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, min_length=2)
    last_name = forms.CharField(required=True, min_length=2)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def clean(self):
        p1 = self.cleaned_data.get("password")
        p2 = self.cleaned_data.get("password_again")
        if p1 != p2:
            raise ValidationError("Passwords do not match!")
