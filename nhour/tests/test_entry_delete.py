from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from nhour.models import Entry
from nhour.tests.test_data import TestData


class TestEntryDelete(TestCase):

    def setUp(self):
        data = TestData()
        self.entry = Entry.objects.create(
            week=9,
            year=2015,
            hours=4,
            system=data.test_system,
            project=data.test_project,
            task=data.test_task,
            user=1)
        self.c = Client()
        User.objects.create_user(username="testuser", email="ex@ex.com", password="Testpassword", first_name="Test", last_name="User")
        self.c.login(username="testuser", password="Testpassword")

    def test_nothing_is_deleted_if_invalid_id_is_given(self):
        self.c.post(reverse("delete_entry", args=[self.entry.id + 1]))
        Entry.objects.get(id=self.entry.id)  # Should not fail

    def test_entry_is_deleted_if_existing_id_is_given(self):
        self.c.post(reverse("delete_entry", args=[self.entry.id]))
        self.assertRaises(ObjectDoesNotExist, Entry.objects.get, id=self.entry.id)



