# coding=utf-8
import datetime
from django import template
from django.core.urlresolvers import reverse
from django.db.models import Sum

from nhour.forms import RegularEntryForm
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
def week_start_date(year, week):
    first_date, last_date = date_range_of_week(year, week)
    return first_date.isoformat()


@register.simple_tag
def week_end_date(year, week):
    first_date, last_date = date_range_of_week(year, week)
    return last_date.isoformat()


def _week_difference(year_now, week_now, year, week):
    return (int(year) - int(year_now)) * 52 + int(week) - int(week_now)

@register.simple_tag
def week_difference_today(year, week):
    today = datetime.datetime.today()
    week_now = today.isocalendar()[1]
    year_now = today.year

    return _week_difference(year_now, week_now, year, week)

@register.filter
def add_plus_if_not_negative(number):
    number = int(number)
    if number > 0:
        return "+{} weeks".format(str(number))
    elif number == 0:
        return "This week"
    return "{} weeks".format(str(number))