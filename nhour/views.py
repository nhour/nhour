from decimal import Decimal

import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from nhour.forms import EntryForm, RegisterForm
from nhour.models import Entry, System, Project, Task


def index_redirect(request):
    today = datetime.datetime.today()
    return redirect('edit_week', today.year, today.isocalendar()[1], 1)

def register(request):
    register_form = RegisterForm(instance=User())
    return render(request, "registration/registration_form.html", context={'register_form': register_form})

def delete_entry(request, year, week, user, id):
    try:
        Entry.objects.get(id=id).delete()
    except ObjectDoesNotExist:
        pass
    return redirect('edit_week', year, week, user)

def edit_week(request, year, week, user):
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
        form = EntryForm(instance=Entry(user=user, week=week))
    entries = Entry.objects.filter(week=week, user=user)
    return render(request, "nhour/index.html", context={'entries': entries,
                                                        'week': week,
                                                        'user': user,
                                                        'form': form,
                                                        'year': year})