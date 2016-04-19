from django.contrib.auth.models import User
from django.test import TestCase, Client

from nhour.forms import EntryForm
from nhour.models import Entry, System, Project, Task

from model_mommy import mommy

class TestEntryEditPage(TestCase):

    def setUp(self):
        self.c = Client()
        User.objects.create_user(username="testuser", email="ex@ex.com", password="Testpassword", first_name="Test", last_name="User")
        self.c.login(username="testuser", password="Testpassword")

        self.system_A = mommy.make(System)
        self.system_B = mommy.make(System)
        self.project_B = mommy.make(Project)
        self.task_B = mommy.make(Task)
        self.task_C = mommy.make(Task)

        self.test_entry_1 = mommy.make(Entry, week=9, year=2015, user="1")
        self.test_entry_2 = mommy.make(Entry, week=9, year=2015, user="1")
        self.test_entry_3 = mommy.make(Entry, week=12, year=2015, user="1")
        self.test_entry_4 = mommy.make(Entry, week=9, year=2015, user="12")

    def test_opening_edit_page_with_week_parameter(self):
        self.assertEquals(self.c.get('/edit/2015/9/1/').status_code, 200)
        self.assertEquals(self.c.get('/edit/2015/4/2/').status_code, 200)

    def test_opening_edit_page_of_week_fetches_entries_of_selected_week(self):
        response = self.c.get('/edit/2015/9/1/')
        self.assertTrue(self.test_entry_1 in response.context['entries'] and
                        self.test_entry_2 in response.context['entries'] and
                        self.test_entry_3 not in response.context['entries'])

    def test_opening_edit_page_of_week_fetches_entries_of_selected_week_and_the_right_user(self):

        response = self.c.get('/edit/2015/9/1/')

        self.assertTrue(self.test_entry_1 in response.context['entries'] and
                        self.test_entry_2 in response.context['entries'] and
                        self.test_entry_3 not in response.context['entries'] and
                        self.test_entry_4 not in response.context['entries'])

        response = self.c.get('/edit/2015/9/12/')

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
        self.c.post('/edit/2015/9/1/', data)
        entries_after = Entry.objects.filter(user=1, week=9, year=2015).count()

        self.assertEqual(entries_before + change, entries_after)

    def test_post_to_edit_page_creates_a_new_entry(self):
        self.post_to_edit_page_and_check_change({'hours': [u'5'],
                                                 'project': [self.project_B.id],
                                                 'system': [self.system_B.id],
                                                 'task': [self.task_B.id],
                                                 'entry_id': ["None"]}, 1)

    def test_post_to_edit_page_creates_a_new_entry_without_project(self):
        self.post_to_edit_page_and_check_change({'hours': ['5'],
                                                 'project': [''],
                                                 'system': [self.system_B.id],
                                                 'task': [self.task_B.id],
                                                'entry_id': ["None"]}, 1)

    def test_post_to_edit_page_without_a_task_creates_nothing(self):
        self.post_to_edit_page_and_check_change({'hours': ['3'],
                                                 'project': [''],
                                                 'system': [self.system_B.id],
                                                 'task': [''],
                                                 'entry_id': ["None"]}, 0)

        self.post_to_edit_page_and_check_change({'hours': ['3'],
                                                 'project': [self.project_B.id],
                                                 'system': [self.system_B.id],
                                                 'task': [''],
                                                 'entry_id': ["None"]}, 0)

    def test_post_to_edit_page_without_a_system_creates_nothing(self):
        self.post_to_edit_page_and_check_change({'hours': ['3'],
                                                 'project': [self.project_B.id],
                                                 'system': [''],
                                                 'task': [self.task_B.id],
                                                 'entry_id': ["None"]}, 0)

    def test_edit_page_with_selected_entry_returns_a_page_with_the_selected_entry_editable(self):
        response = self.c.get('/edit/{}/'.format(self.test_entry_1.id))
        self.assertEqual(response.context['form'].instance.id, self.test_entry_1.id)
class TestEditTemplateContext:

    def setUp(self):
        self.response = self.c.get('/edit/2015/9/1/')

    def test_total_hours_are_calculated(self):
        self.assertEquals(self.response.context['total_hours'], 5)

    def test_week_is_passed_into_edit_template(self):
        self.assertEquals(self.response.context['week'], 9)

    def test_year_is_passed_into_edit_template(self):
        self.assertEquals(self.response.context['year'], 2015)

    def test_user_is_passed_into_edit_template(self):
        self.assertEquals(self.response.context['user'], '1')
