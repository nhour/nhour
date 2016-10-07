from django.test import TestCase
from django.core.management import call_command
import django.core.mail as mail

from nhour.tests.factories import UserFactory

from datetime import datetime, timedelta

from django.conf import settings

class TestEntryDelete(TestCase):

    def _user_with_unfinished_weeks(self):
        user = UserFactory()
        user.date_joined = datetime.now() - timedelta(weeks=1)
        user.save()
        return user

    def test_user_is_sent_email_if_has_unfinished_weeks(self):
        user = self._user_with_unfinished_weeks()
        call_command('reminder_email')
        self.assertEqual(len(mail.outbox), 1)

    def test_user_is_not_sent_email_if_has_no_unfinished_weeks(self):
        user = UserFactory()
        call_command('reminder_email')
        self.assertEqual(len(mail.outbox), 0)

    def test_correct_user_is_sent_email(self):
        user = self._user_with_unfinished_weeks()
        call_command('reminder_email')
        self.assertIn(user.email, mail.outbox[0].to)

    def test_email_sender_is_correct(self):
        user = self._user_with_unfinished_weeks()
        call_command('reminder_email')
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_SENDER)

    def test_inactive_user_is_not_sent_email(self):
        user = self._user_with_unfinished_weeks()
        user.is_active = False
        user.save()
        call_command('reminder_email')
        self.assertEqual(len(mail.outbox), 0)

