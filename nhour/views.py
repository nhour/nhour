import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.forms import Form
from django.shortcuts import render, redirect, get_object_or_404

from nhour.forms import RegularEntryForm, RegisterForm, entry_form_factory, SpecialEntryForm
from nhour.models import SpecialEntry, RegularEntry, Entry


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
        entry = RegularEntry(year=year, week=week, user=User.objects.get(id=user))
    else:
        entry = SpecialEntry(year=year, week=week, user=User.objects.get(id=user))
    return entry


def _render_page_with_form(form: Form, request, user, week, year):
    regular_entries = RegularEntry.objects.filter(week=week, user=user)
    special_entries = SpecialEntry.objects.filter(week=week, user=user)

    return render(request, "nhour/index.html", context={'entries': regular_entries,
                                                        'special_entries': special_entries,
                                                        'week': week,
                                                        'user': user,
                                                        'form': form,
                                                        'regular_entry': isinstance(form, RegularEntryForm),
                                                        'year': year,
                                                        'total_hours': regular_entries.aggregate(Sum('hours'))['hours__sum']})


@login_required
def save_entry(request, id):
    entry = Entry.objects.get(id=id)
    form = entry_form_factory(entry, request.POST)
    return _submit_form(request, form)


def _submit_form(request, form):
    if form.is_valid():
        form.save()
        return redirect('edit_week', form.instance.year, form.instance.week, form.instance.user.id)
    else:
        return _render_page_with_form(form, request, form.instance.user.id, form.instance.week, form.instance.year)


def create_entry(request):
    is_special = "True" == request.GET.get("special", "False")
    if is_special:
        form = SpecialEntryForm(request.POST)
    else:
        form = RegularEntryForm(request.POST)
    return _submit_form(request, form)



def _redirect_to_entry_list(entry):
    return redirect(reverse("edit_week", args=[entry.year, entry.week, entry.user.id]))


@login_required()
def delete_entry(request, entry_id):
    deleted_entry = get_object_or_404(Entry, id=entry_id)
    deleted_entry.delete()
    return _redirect_to_entry_list(deleted_entry)
