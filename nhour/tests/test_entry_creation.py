from random import Random

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

import nhour
from nhour.forms import RegularEntryForm
from nhour.models import Entry, RegularEntry, System, Project, Task
from nhour.tests.factories import RegularEntryFactory, SpecialEntryFactory


class TestEntryEditPage(TestCase):
    def setUp(self):
        self.c = Client()
        User.objects.create_user(username="testuser", email="ex@ex.com", password="Testpassword", first_name="Test",
                                 last_name="User")
        self.c.login(username="testuser", password="Testpassword")

    def test_opening_edit_page(self):
        entries = RegularEntryFactory.create_batch(10)
        for entry in entries:
            self.assertEquals(self.c.get(self._edit_page_of_entry(entry)).status_code, 200)

    def test_opening_edit_page_of_week_fetches_entries_of_selected_week(self):
        test_entry_1 = RegularEntryFactory(year=2015, week=9)
        test_entry_2 = RegularEntryFactory(year=2015, week=9, user=test_entry_1.user)
        test_entry_3 = RegularEntryFactory(year=2015, week=10, user=test_entry_1.user)

        response = self.c.get('/edit/2015/9/{}/'.format(test_entry_1.user.id))

        self.assertIn(test_entry_1, response.context['entries'])
        self.assertIn(test_entry_2, response.context['entries'])
        self.assertNotIn(test_entry_3, response.context['entries'])

    def test_opening_edit_page_of_week_fetches_entries_of_selected_week_and_the_right_user(self):
        entry_1 = RegularEntryFactory()
        entry_2 = RegularEntryFactory(user=entry_1.user, week=entry_1.week)
        entry_3 = RegularEntryFactory(user=entry_1.user)

    def test_entry_project_is_not_required(self):
        self.assertEquals({}, RegularEntryForm(instance=RegularEntryFactory()).errors)

    def post_to_edit_page_and_check_change(self, data, change):
        self.c.post("/create/", data=data)
        entries_after = Entry.objects.all().count()

        self.assertEqual(change, entries_after)

    def _entry_into_post_data(self, entry):
        data_as_dictionary = RegularEntryForm(instance=entry).initial
        data_as_post = {key: [str(data) if data else ""] for key, data in data_as_dictionary.items()}
        return data_as_post

    def test_post_to_edit_page_creates_a_new_entry(self):
        self.post_to_edit_page_and_check_change(self._entry_into_post_data(RegularEntryFactory.build()), 1)

    def test_post_to_edit_page_creates_a_new_entry_without_project(self):
        entry = RegularEntryFactory.build()
        post_data = self._entry_into_post_data(entry)
        post_data["project"] = [""]
        self.post_to_edit_page_and_check_change(post_data, 1)

    def test_post_to_edit_page_without_a_task_creates_nothing(self):
        entry = RegularEntryFactory.build()
        post_data = self._entry_into_post_data(entry)
        post_data["task"] = [""]
        self.post_to_edit_page_and_check_change(post_data, 0)

    def test_post_to_edit_page_without_a_system_creates_nothing(self):
        entry = RegularEntryFactory.build()
        post_data = self._entry_into_post_data(entry)
        post_data["system"] = [""]
        self.post_to_edit_page_and_check_change(post_data, 0)

    def test_edit_page_with_selected_entry_returns_a_page_with_the_selected_entry_editable(self):
        t = RegularEntryFactory()
        response = self.c.get(self._edit_page_of_entry(t))
        self.assertEqual(response.context['form'].instance.id, t.id)

    def _edit_page_of_entry(self, t):
        return '/edit/{}/{}/{}/?entry={}'.format(t.year, t.week, t.user.id, t.id)

    def test_editing_entry_changes_hours(self):
        test_entry = RegularEntryFactory()
        post_data = self._entry_into_post_data(test_entry)
        post_data["hours"] = ["15"]
        self.c.post(reverse("save_entry", args=[test_entry.id]), data=post_data)
        test_entry.refresh_from_db()
        self.assertEqual(test_entry.hours, 15)