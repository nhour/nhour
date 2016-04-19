import datetime
from django.test import TestCase

from nhour.templatetags.tags import previous_week_url, next_week_url, week_name
from nhour.utils import increment_week, decrement_week, date_range_of_week


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

    def test_previous_week_url_tag_generates_a_url_pointing_to_the_previous_week(self):
        self.assertEqual(previous_week_url(2015, 33, 1), '/edit/2015/32/1/')
        self.assertEqual(previous_week_url("2015", "33", "1"), '/edit/2015/32/1/')

    def test_next_week_url_tag_generates_a_url_pointing_to_the_next_week(self):
        self.assertEqual(next_week_url(2015, 33, 1), '/edit/2015/34/1/')
        self.assertEqual(next_week_url("2015", "33", "1"), '/edit/2015/34/1/')

class TestWeekNameGeneration(TestCase):

    def test_date_range_of_week_start_and_end_dates_are_correct(self):
        start, end = date_range_of_week(2016, 10)
        self.assertTrue(date_range_of_week(2016, 10), (datetime.date(2016, 3, 7), datetime.date(2016, 3, 13)))

    def test_date_range_is_in_the_name(self):
        self.assertIn("2016-03-07 – 2016-03-13", week_name("2016", "10"))