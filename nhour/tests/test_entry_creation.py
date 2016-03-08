from django.test import TestCase, Client

from nhour.forms import EntryForm
from nhour.models import Entry, System, Project, Task


class TestEntryEditPage(TestCase):

    def setUp(self):
        self.c = Client()

        self.system_A = System.objects.create(name="A")
        self.system_B = System.objects.create(name="B")
        self.project_B = Project.objects.create(name="B")
        self.task_B = Task.objects.create(name="B")
        self.task_C = Task.objects.create(name="C")

        self.test_entry_1 = Entry(week=9, year=2015, system=self.system_A, project=self.project_B, task=self.task_C, user="1", hours=3)
        self.test_entry_1.save()

        self.test_entry_2 = Entry(week=9, year=2015, system=self.system_B, project=self.project_B, task=self.task_B, user="1", hours=2)
        self.test_entry_2.save()

        self.test_entry_3 = Entry(week=10, year=2015, system=self.system_B, project=self.project_B, task=self.task_B, user="1", hours=1)
        self.test_entry_3.save()

        self.test_entry_4 = Entry(week=9, year=2015, system=self.system_B, project=self.project_B, task=self.task_B, user="12", hours=2)
        self.test_entry_4.save()

    def test_opening_edit_page_with_week_parameter(self):
        self.assertEquals(self.c.get('/edit/2015/9/1').status_code, 200)
        self.assertEquals(self.c.get('/edit/2015/4/2').status_code, 200)

    def test_opening_edit_page_of_week_fetches_entries_of_selected_week(self):
        response = self.c.get('/edit/2015/9/1')
        self.assertTrue(self.test_entry_1 in response.context['entries'] and
                        self.test_entry_2 in response.context['entries'] and
                        self.test_entry_3 not in response.context['entries'])

    def test_opening_edit_page_of_week_fetches_entries_of_selected_week_and_the_right_user(self):

        response = self.c.get('/edit/2015/9/1')

        self.assertTrue(self.test_entry_1 in response.context['entries'] and
                        self.test_entry_2 in response.context['entries'] and
                        self.test_entry_3 not in response.context['entries'] and
                        self.test_entry_4 not in response.context['entries'])

        response = self.c.get('/edit/2015/9/12')

        self.assertTrue(self.test_entry_1 not in response.context['entries'] and
                        self.test_entry_2 not in response.context['entries'] and
                        self.test_entry_3 not in response.context['entries'] and
                        self.test_entry_4 in response.context['entries'])

    def test_entry_project_is_not_required(self):
        self.assertTrue(EntryForm({'system': self.system_B.id,
                                   'task': self.task_B.id,
                                   'hours': '3',
                                   'project': '',
                                   }).is_valid())

    def post_to_edit_page_and_check_change(self, data, change):
        entries_before = Entry.objects.filter(user=1, week=9, year=2015).count()
        self.c.post('/edit/2015/9/1', data)
        entries_after = Entry.objects.filter(user=1, week=9, year=2015).count()

        self.assertEqual(entries_before + change, entries_after)

    def test_post_to_edit_page_creates_a_new_entry(self):
        self.post_to_edit_page_and_check_change({'hours': [u'5'],
                                                 'project': [self.project_B.id],
                                                 'system': [self.system_B.id],
                                                 'task': [self.task_B.id],}, 1)

    def test_post_to_edit_page_creates_a_new_entry_without_project(self):
        self.post_to_edit_page_and_check_change({'hours': ['5'],
                                                 'project': [''],
                                                 'system': [self.system_B.id],
                                                 'task': [self.task_B.id]}, 1)

    def test_post_to_edit_page_without_a_task_creates_nothing(self):
        self.post_to_edit_page_and_check_change({'hours': ['3'],
                                                 'project': [''],
                                                 'system': [self.system_B.id],
                                                 'task': ['']}, 0)

        self.post_to_edit_page_and_check_change({'hours': ['3'],
                                                 'project': [self.project_B.id],
                                                 'system': [self.system_B.id],
                                                 'task': ['']}, 0)

    def test_post_to_edit_page_without_a_system_creates_nothing(self):
        self.post_to_edit_page_and_check_change({'hours': ['3'],
                                                 'project': [self.project_B.id],
                                                 'system': [''],
                                                 'task': [self.task_B.id]}, 0)
class TestEditTemplateContext:

    def setUp(self):
        self.response = self.c.get('/edit/2015/9/1')

    def test_total_hours_are_calculated(self):
        self.assertEquals(self.response.context['total_hours'], 5)

    def test_week_is_passed_into_edit_template(self):
        self.assertEquals(self.response.context['week'], 9)

    def test_year_is_passed_into_edit_template(self):
        self.assertEquals(self.response.context['year'], 2015)

    def test_user_is_passed_into_edit_template(self):
        self.assertEquals(self.response.context['user'], '1')

