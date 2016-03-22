from django import forms
from django.forms import ModelForm, Select

from nhour.models import Entry, System, Project, Task


class EntryForm(ModelForm):
    system = forms.ModelChoiceField(System.objects.all(), empty_label="Select a system", error_messages={'required': 'Required!'})
    project = forms.ModelChoiceField(Project.objects.all(), empty_label="Select a project", required=False)
    task = forms.ModelChoiceField(Task.objects.all(), empty_label="Select a task", error_messages={'required': 'Required!'})
    user = forms.HiddenInput()
    week = forms.HiddenInput()
    year = forms.HiddenInput()
    class Meta:
        model = Entry
        fields = ['system', 'project', 'task']