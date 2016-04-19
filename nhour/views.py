from decimal import Decimal

import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from nhour.forms import EntryForm, RegisterForm
from nhour.models import Entry, System, Project, Task

@login_required()
def index_redirect(request):
    today = datetime.datetime.today()
    return redirect('edit_week', today.year, today.isocalendar()[1], request.user.id)


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.is_active = False
            new_user.save()
    else:
        register_form = RegisterForm(instance=User())
    return render(request, "registration/register.html", context={'register_form': register_form})

def edit_entry(request, entry=None):
    entry_object = get_object_or_404(Entry, id=entry)
    return edit_week(request, entry_object.year, entry_object.week, entry_object.user, entry)


def _redirect_to_entry_list(entry):
    return redirect(reverse("edit_week", args=[entry.year, entry.week, entry.user]))


@login_required()
def save_entry(request, entry_id):
    form = EntryForm(request.POST, instance=get_object_or_404(Entry, id=entry_id))
    if form.is_valid():
        form.save()
    entry = form.instance
    return _redirect_to_entry_list(entry)

@login_required()
def delete_entry(request, entry_id):
    deleted_entry = get_object_or_404(Entry, id=entry_id)
    deleted_entry.delete()
    return _redirect_to_entry_list(deleted_entry)

@login_required()
def edit_week(request, year, week, user, entry=None):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.hours = Decimal(request.POST['hours'])
            new_entry.user = user
            new_entry.week = week
            new_entry.year = year
            new_entry.save()
            return redirect('edit_week', year, week, user)
    else:
        try:
            editable_entry = Entry.objects.get(id=entry)
        except ObjectDoesNotExist:
            editable_entry = Entry(user=user, week=week)
        form = EntryForm(instance=editable_entry)
    entries = Entry.objects.filter(week=week, user=user)
    return render(request, "nhour/index.html", context={'entries': entries,
                                                        'week': week,
                                                        'user': user,
                                                        'form': form,
                                                        'year': year,
                                                        'total_hours': entries.aggregate(Sum('hours'))['hours__sum']})