from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from nhour.tests.factories import UserFactory


class TestIndex(TestCase):

    def test_user_object_is_passed_into_template(self):
        user = UserFactory()
        c = Client()
        c.force_login(user)
        response = c.get("/", follow=True)
        self.assertIsInstance(response.context["user"], User)