from django.contrib.auth.models import User

from nhour.models import System, Project, Task


class TestData:

    def __init__(self):
        self.test_system = System.objects.create(name='Test1')
        self.test_project = Project.objects.create(name='Test2')
        self.test_task = Task.objects.create(name='Test3')