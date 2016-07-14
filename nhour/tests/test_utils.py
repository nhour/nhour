import datetime
from django.test import TestCase

from nhour.models import RegularEntry, SpecialEntry, CompletedWeek
from nhour.templatetags.tags import previous_week_url, next_week_url, week_start_date, _week_difference
from nhour.tests.factories import RegularEntryFactory, UserFactory, SpecialEntryFactory, SystemFactory
from nhour.utils import increment_week, decrement_week, date_range_of_week, entry_shortcuts, unfinished_weeks_of_user
from nhour.views import _sum_entry_hours


class TestWeekPaging(TestCase):
    def test_week_is_incremented_when_within_1_and_51(self):
        self.assertEquals((2013, 5), increment_week(2013, 4))
        self.assertEquals((2013, 52), increment_week(2013, 51))
        self.assertEquals((2013, 2), increment_week(2013, 1))

    def test_year_is_incremented_and_week_set_to_1_when_week_is_52(self):
        self.assertEquals((2014, 1), increment_week(2013, 52))

    def test_week_is_decremented_when_within_2_and_52(self):
        self.assertEquals((2013, 3), decrement_week(2013, 4))
        self.assertEquals((2013, 51), decrement_week(2013, 52))
        self.assertEquals((2013, 1), decrement_week(2013, 2))

    def test_year_is_decremented_when_week_is_1_and_week_is_set_to_52(self):
        self.assertEquals((2013, 52), decrement_week(2014, 1))

    def test_previous_week_url_tag_generates_a_url_pointing_to_the_previous_week(
            self):
        self.assertEqual(previous_week_url(2015, 33, 1), '/edit/2015/32/1/')
        self.assertEqual(
            previous_week_url("2015", "33", "1"), '/edit/2015/32/1/')

    def test_next_week_url_tag_generates_a_url_pointing_to_the_next_week(self):
        self.assertEqual(next_week_url(2015, 33, 1), '/edit/2015/34/1/')
        self.assertEqual(next_week_url("2015", "33", "1"), '/edit/2015/34/1/')


class TestWeekNameGeneration(TestCase):
    def test_date_range_of_week_start_and_end_dates_are_correct(self):
        start, end = date_range_of_week(2016, 10)
        self.assertTrue(
            date_range_of_week(2016, 10),
            (datetime.date(2016, 3, 7), datetime.date(2016, 3, 13)))

    def test_date_range_is_in_the_name(self):
        self.assertIn("2016-03-07", week_start_date("2016", "10"))

    def test_week_difference(self):

        difference1 = _week_difference("2013", "5", "2013", "6")
        difference2 = _week_difference("2013", "5", "2013", "2")
        difference3 = _week_difference("2013", "5", "2012", "5")
        difference4 = _week_difference("2013", "5", "2013", "5")
        difference5 = _week_difference("2013", "5", "2012", "7")

        self.assertEqual(1, difference1)
        self.assertEqual(-3, difference2)
        self.assertEqual(-52, difference3)
        self.assertEqual(0, difference4)
        self.assertEqual(-50, difference5)


class TestSumEntryHours(TestCase):
    def test_empty_entry_values_are_ok(self):
        RegularEntryFactory(hours=3)
        self.assertEqual(3, _sum_entry_hours(RegularEntry.objects.all(),
                                             SpecialEntry.objects.all()))

    def test_entry_hours_are_summed_together(self):
        RegularEntryFactory(hours=3)
        RegularEntryFactory(hours=6)
        SpecialEntryFactory(hours=6)

        self.assertEqual(15, _sum_entry_hours(RegularEntry.objects.all(),
                                              SpecialEntry.objects.all()))


class TestShortcuts(TestCase):
    def test_no_shortcuts_if_no_previous_entries(self):
        self.assertEqual(0, len(entry_shortcuts(UserFactory(), 2015, 22)))

    def test_shortcuts_are_generated_from_previous_and_future_weeks(self):
        user = UserFactory()
        RegularEntryFactory.create_batch(3, user=user, year="2015", week="20")
        RegularEntryFactory.create_batch(5, user=user, year="2015", week="21")
        RegularEntryFactory.create_batch(1, user=user, year="2015", week="22")
        RegularEntryFactory.create_batch(1, user=user, year="2015", week="23")
        self.assertEqual(9, len(entry_shortcuts(user, 2015, 22)))

    def test_only_shortcuts_from_the_specified_user_are_returned(self):
        right_user = UserFactory.create()
        wrong_user = UserFactory.create()
        RegularEntryFactory.create_batch(
            3, user=right_user, year="2015",
            week="20")
        RegularEntryFactory.create_batch(
            5, user=wrong_user, year="2015",
            week="21")
        self.assertEqual(3, len(entry_shortcuts(right_user, 2015, 22)))

    def test_no_duplicates_are_returned(self):
        entry = RegularEntryFactory(user=UserFactory(), year="2015", week="20")
        entry2 = RegularEntryFactory(user=entry.user,
                                     system=entry.system,
                                     project=entry.project,
                                     task=entry.task,
                                     year="2014")

        self.assertEqual(2, RegularEntry.objects.count())
        self.assertEqual(1,
                         len(entry_shortcuts(user=entry.user,
                                             year=entry.year,
                                             week=int(entry.week) - 1)))


class TestUnfinishedWeeks(TestCase):
    def test_all_weeks_since_registration_if_no_completed_weeks(self):
        user = UserFactory()
        for week_difference in range(0, 150):
            user.date_joined = datetime.datetime.today() - datetime.timedelta(
                weeks=week_difference)
            user.save()
            self.assertEquals(
                len(unfinished_weeks_of_user(user)), week_difference)

    def test_does_not_return_current_week(self):
        user = UserFactory()
        user.date_joined = datetime.datetime(2014, 9, 1)
        today = datetime.datetime.now()
        self.assertNotIn(
            (today.year,
             today.isocalendar()[1]), unfinished_weeks_of_user(user))

    def test_does_not_return_completed_weeks(self):
        user = UserFactory()
        user.date_joined = datetime.datetime(2014, 9, 1)
        CompletedWeek.objects.create(year=2014, week=50, user=user)
        CompletedWeek.objects.create(year=2015, week=40, user=user)
        self.assertNotIn((2014, 50), unfinished_weeks_of_user(user))
        self.assertNotIn((2015, 40), unfinished_weeks_of_user(user))
        self.assertIn((2015, 41), unfinished_weeks_of_user(user))
        self.assertIn((2015, 39), unfinished_weeks_of_user(user))
        self.assertIn((2014, 49), unfinished_weeks_of_user(user))
        self.assertIn((2014, 51), unfinished_weeks_of_user(user))
