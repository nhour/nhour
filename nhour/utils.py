import datetime

def increment_week(year, week):
    if week == 52:
        return year + 1, 1

    return year, week + 1


def decrement_week(year, week):
    if week == 1:
        return year - 1, 52
    return year, week - 1

def date_range_of_week(year, week):

    first_day_of_the_week = datetime.datetime.strptime("{} {} {}".format(year, int(week), 1), "%Y %W %w").date()
    last_day_of_the_week = datetime.datetime.strptime("{} {} {}".format(year, int(week), 0), "%Y %W %w").date()

    return first_day_of_the_week, last_day_of_the_week
