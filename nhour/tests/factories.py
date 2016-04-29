import string
from random import Random

import factory
from django.contrib.auth.models import User
from factory import Factory, DjangoModelFactory
from factory.fuzzy import FuzzyText


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    first_name = factory.Faker('first_name', locale="fi_FI")
    last_name = factory.Faker('last_name')
    email = factory.Faker('profile')
    username = FuzzyText(prefix="ä", length=Random().randint(3, 20))
    password = FuzzyText(prefix="ä", length=Random().randint(8, 20))