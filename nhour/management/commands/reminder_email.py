from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from nhour.utils import unfinished_weeks_of_users
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--send',
            action='store_true',
            default=False,
            dest='send',
            help='print a list of the email addresses that would recieve a reminder message',
        )
    def handle(self, *args, **options):
        unfinished_users_and_weeks = unfinished_weeks_of_users(User.objects.filter(is_active=True))
        for user, unfinished_weeks in unfinished_users_and_weeks:

            if not user.email:
                continue

            if unfinished_weeks:
              print(user.email, unfinished_weeks)

              if options["send"]:
                  send_mail(
                      subject='You have unfinished weeks!',
                      message='You have unfinished weeks! Please complete them as soon as possible.\n{}'.format(settings.EMAIL_URL_LINK),
                      from_email=settings.EMAIL_SENDER,
                      recipient_list=[user.email]
                  )

