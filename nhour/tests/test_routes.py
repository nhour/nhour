import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client


class TestRoutes(TestCase):

    def setUp(self):
        self.c = Client()

    # def test_user_is_sent_to_login_page_when_accessing_main_page(self):
    #     def access_page_and_check_if_in_login(url):
    #         root = self.c.get(url, follow=True)
    #         #self.assertTrue(root.request.url.startswith("/login?next="))
    #         self.assertEqual(root.request.status, "200")
    #
    #     access_page_and_check_if_in_login('/')
    #     access_page_and_check_if_in_login('/edit/2009/09/4')


    def test_if_user_has_no_sent_entries_they_are_redirected_to_the_latest_weeks_page(self):
        User.objects.create_user(username="testuser", email="ex@ex.com", password="Testpassword", first_name="Test", last_name="User")
        self.c.login(username="testuser", password="Testpassword")
        root = self.c.get('/')
        now = datetime.datetime.today()
        current_week = now.isocalendar()[1]
        self.assertEqual(root.status_code, 302)
        self.assertEqual(root.url, "/edit/{}/{}/1/".format(now.year, current_week))