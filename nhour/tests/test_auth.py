from django.core.urlresolvers import reverse
from django.test import Client
from django_webtest import WebTest

from nhour.tests.factories import UserFactory


class TestAuthorization(WebTest):

    def test_login_with_valid_user(self):
        user = 
        login_form = self.app.get(reverse('login')).form
        login_form["username"] = user.username
        login_form["password"] = user.password
        response = login_form.submit()

        self.assertEqual(response.context["user"].username, user.username)