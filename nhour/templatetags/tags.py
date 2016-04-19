# coding=utf-8
from django import template
from django.core.urlresolvers import reverse
from django.db.models import Sum

from nhour.forms import EntryForm
from nhour.models import System, Project, Task, Entry
from nhour.utils import decrement_week, increment_week, date_range_of_week

register = template.Library()

def _arguments_into_int(user, week, year):
    year = int(year)
    week = int(week)
    user = int(user)
    return user, week, year


@register.simple_tag
def previous_week_url(year, week, user):
    user, week, year = _arguments_into_int(user, week, year)
    previous_week_year, previous_week = decrement_week(year, week)
    return reverse('edit_week', args=[previous_week_year, previous_week, user])


@register.simple_tag
def next_week_url(year, week, user):
    user, week, year = _arguments_into_int(user, week, year)
    next_week_year, next_week = increment_week(year, week)
    return reverse('edit_week', args=[next_week_year, next_week, user])

@register.simple_tag
def week_name(year, week):
    first_date, last_date = date_range_of_week(year, week)
    return "{} – {}".format(first_date.isoformat(), last_date.isoformat())