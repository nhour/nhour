from django.core.exceptions import ValidationError
from django.test import TestCase
from nhour.models import Entry, Task, Project, System


class TestEntryValidation(TestCase):

    def setUp(self):
        self.test_system = System.objects.create(name='Test1')
        self.test_project = Project.objects.create(name='Test2')
        self.test_task = Task.objects.create(name='Test3')

    def test_entry_must_contain_a_week_and_a_year(self):
        self.failUnlessRaises(ValidationError, Entry(
            week=9,
            year='',
            hours=4,
            system=self.test_system,
            project=self.test_project,
            task=self.test_task,
            user=1).full_clean)

        self.failUnlessRaises(ValidationError, Entry(
            week='',
            year=2015,
            hours=4,
            system=self.test_system,
            project=self.test_project,
            task=self.test_task,
            user=1).full_clean)

        Entry(
            week=9,
            year=2015,
            hours=4,
            system=self.test_system,
            project=self.test_project,
            task=self.test_task,
            user=1).full_clean()

    def test_system_is_printed_in_human_readable_form(self):
        self.assertEqual(self.test_system.__str__(), "Test1")

    def test_project_is_printed_in_human_readable_form(self):
        self.assertEqual(self.test_project.__str__(), "Test2")

    def test_system_is_printed_in_human_readable_form(self):
        self.assertEqual(self.test_task.__str__(), "Test3")


