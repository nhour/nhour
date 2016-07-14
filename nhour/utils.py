import datetime
from operator import itemgetter

from django.utils.datastructures import OrderedSet

from nhour.models import RegularEntry, System, Task, Project, CompletedWeek


def increment_week(year, week):
    if week == 52:
        return year + 1, 1

    return year, week + 1


def decrement_week(year, week):
    if week == 1:
        return year - 1, 52
    return year, week - 1


def date_range_of_week(year, week):
    first_day_of_the_week = datetime.datetime.strptime("{} {} {}".format(
        year, int(week), 1), "%Y %W %w").date()
    last_day_of_the_week = datetime.datetime.strptime("{} {} {}".format(
        year, int(week), 0), "%Y %W %w").date()

    return first_day_of_the_week, last_day_of_the_week


def entry_shortcuts(user, year, week):
    # Couldn't figure out how to do these using the database.
    max_results = 150
    max_shortcuts = 15

    entires_with_ids = RegularEntry.objects \
               .filter(user=user) \
               .exclude(year=year, week=week) \
               .values("system", "project", "task")[:max_results]
    tuple_results = [(entry["system"], entry["project"], entry["task"])
                     for entry in entires_with_ids]
    unique_results = list(OrderedSet(tuple_results))[:15]
    unordered_shortcuts = \
    [{"system": System.objects.get(id=e[0]),
      "project": Project.objects.filter(id=e[1]).first(),
      "task": Task.objects.get(id=e[2])} for e in unique_results]

    def sorter(k):
        if k["project"]:
            return k["system"].name, k["project"].name, k["task"].name
        return k["system"].name, k["task"].name

    return sorted(unordered_shortcuts, key=sorter)


def _weeks_since(start_date):
    date = start_date.date()
    dates = []
    today = datetime.datetime.today()
    week_first_day, week_last_day = date_range_of_week(today.year,
                                                       today.isocalendar()[1])
    while date < week_first_day:
        dates.append((date.year, date.isocalendar()[1]))
        date += datetime.timedelta(weeks=1)

    return dates


def unfinished_weeks_of_user(user):
    joined = user.date_joined
    weeks = set(_weeks_since(joined))
    completed_weeks = {
        (complete_week.year, complete_week.week)
        for complete_week in CompletedWeek.objects.filter(user=user)
    }

    return weeks - completed_weeks
