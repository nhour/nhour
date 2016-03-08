import datetime
from django.test import TestCase, Client


class TestRoutes(TestCase):

    def test_if_user_has_no_sent_entries_they_are_redirected_to_the_latest_weeks_page(self):
        c = Client()
        root = c.get('/')
        now = datetime.datetime.today()
        current_week = now.isocalendar()[1]
        self.assertEqual(root.status_code, 302)
        self.assertEqual(root.url, "/edit/{}/{}/1".format(now.year, current_week))