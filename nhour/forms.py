from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, Select, Form
from nhour.models import Entry, System, Project, Task


class EntryForm(ModelForm):
    system = forms.ModelChoiceField(System.objects.all(), empty_label="Select a system")
    project = forms.ModelChoiceField(Project.objects.all(), empty_label="Select a project", required=False)
    task = forms.ModelChoiceField(Task.objects.all(), empty_label="Select a task")
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)
    user = forms.HiddenInput()
    week = forms.HiddenInput()
    year = forms.HiddenInput()
    class Meta:
        model = Entry
        fields = ['system', 'project', 'task', 'comment']

class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_again = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, min_length=2)
    last_name = forms.CharField(required=True, min_length=2)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']