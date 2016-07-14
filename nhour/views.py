import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.forms import Form
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from nhour.forms import RegularEntryForm, RegisterForm, entry_form_factory, SpecialEntryForm
from nhour.models import SpecialEntry, RegularEntry, Entry, System, Task, Project, Activity, CompletedWeek
from nhour.utils import entry_shortcuts, unfinished_weeks_of_user


@login_required()
def index_redirect(request):
    unfinished_weeks = unfinished_weeks_of_user(request.user)
    if unfinished_weeks:
        oldest_unfinished_week_year, oldest_unfinished_week = sorted(
            unfinished_weeks)[0]
        return edit_week(request, oldest_unfinished_week_year,
                         oldest_unfinished_week, request.user.id)
    else:
        today = datetime.datetime.today()
        return edit_week(request, today.year, today.isocalendar()[1],
                         request.user.id)


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            return redirect("thanks")
    else:
        register_form = RegisterForm()
    return render(request,
                  "registration/register.html",
                  context={'register_form': register_form})


def thank_you(request):
    return render(request, "registration/thanks.html")


@login_required()
def edit_week(request, year, week, user):

    entry_id = request.GET.get("entry", None)
    is_special = "True" == request.GET.get("special", "False")
    regular = not is_special

    if entry_id:
        entry = _get_old_entry(entry_id)
    else:
        entry = _make_new_entry(regular, user, week, year)

    form = entry_form_factory(entry)
    return _render_page_with_form(form, request, user, week, year)


def _get_old_entry(entry_id):
    return Entry.objects.get(id=entry_id)


def _make_new_entry(regular, user, week, year):
    if regular:
        entry = RegularEntry(year=year,
                             week=week,
                             user=User.objects.get(id=user))
    else:
        entry = SpecialEntry(year=year,
                             week=week,
                             user=User.objects.get(id=user))
    return entry


def _render_page_with_form(form: Form, request, user, week, year):
    regular_entries = RegularEntry.objects.filter(week=week, user=user)
    special_entries = SpecialEntry.objects.filter(week=week, user=user)

    systems = serializers.serialize("json", System.objects.all())
    projects = serializers.serialize("json", Project.objects.all())
    tasks = serializers.serialize("json", Task.objects.all())
    activities = serializers.serialize("json", Activity.objects.all())

    user_object = User.objects.get(id=user)
    unfinished_weeks = unfinished_weeks_of_user(user_object)
    shortcuts = entry_shortcuts(user_object, int(year), int(week))
    week_complete = CompletedWeek.objects.filter(
        user=user_object, week=week, year=year).count() > 0

    return render(request,
                  "nhour/index.html",
                  context={'entries': regular_entries,
                           'special_entries': special_entries,
                           'week': week,
                           'user': user_object,
                           'form': form,
                           'regular_entry': isinstance(form, RegularEntryForm),
                           'year': year,
                           'total_hours': _sum_entry_hours(regular_entries,
                                                           special_entries),
                           'systems': systems,
                           'projects': projects,
                           'tasks': tasks,
                           'activities': activities,
                           'shortcuts': shortcuts,
                           'week_complete': week_complete,
                           'unfinished_weeks': sorted(list(unfinished_weeks))})


def _sum_entry_hours(regular_entries, special_entries):

    sum_special = special_entries.aggregate(Sum('hours'))['hours__sum']
    sum_regular = regular_entries.aggregate(Sum('hours'))['hours__sum']

    sum_special = sum_special if sum_special else 0
    sum_regular = sum_regular if sum_regular else 0
    return sum_special + sum_regular


@login_required
def save_entry(request, id):
    entry = Entry.objects.get(id=id)
    form = entry_form_factory(entry, request.POST)
    return _submit_form(request, form)


def _submit_form(request, form):
    if form.is_valid():
        form.save()
        return redirect('edit_week', form.instance.year, form.instance.week,
                        form.instance.user.id)
    else:
        return _render_page_with_form(form, request, form.instance.user.id,
                                      form.instance.week, form.instance.year)


@login_required
def create_entry(request):
    is_special = "True" == request.GET.get("special", "False")
    if is_special:
        form = SpecialEntryForm(request.POST)
    else:
        form = RegularEntryForm(request.POST)
    return _submit_form(request, form)


def _redirect_to_entry_list(entry):
    return redirect(reverse("edit_week",
                            args=[entry.year, entry.week, entry.user.id]))


@login_required()
def delete_entry(request, entry_id):
    deleted_entry = get_object_or_404(Entry, id=entry_id)
    deleted_entry.delete()
    return _redirect_to_entry_list(deleted_entry)


@login_required
def week_complete(request, year, week, user):
    complete = request.POST.get("complete", 'off')
    user_object = User.objects.get(id=user)
    if complete == 'off':
        _delete_completed_week_if_exists(year, week, user_object)

    if complete == 'on':
        _save_completed_week(year, week, user_object)

    return HttpResponse('Success')


def _save_completed_week(year, week, user):
    CompletedWeek.objects.get_or_create(year=year, week=week, user=user)


def _delete_completed_week_if_exists(year, week, user):
    try:
        CompletedWeek.objects.get(year=year, week=week, user=user).delete()
    except:
        pass
