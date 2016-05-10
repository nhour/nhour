import random

import factory
from django.contrib.auth.models import User
from factory import DjangoModelFactory
from factory.fuzzy import FuzzyText, FuzzyInteger, FuzzyFloat, FuzzyDecimal

from nhour.models import RegularEntry, System, Project, Task, Activity, SpecialEntry


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = FuzzyText(length=random.Random().randint(1, 30))
    password = FuzzyText(length=random.Random().randint(1, 30))
    first_name = FuzzyText(length=random.Random().randint(1, 30))
    last_name = FuzzyText(length=random.Random().randint(1, 30))
    email = factory.LazyAttribute(lambda u: '{}@example.com'.format(u.username))


class SystemFactory(DjangoModelFactory):
    class Meta:
        model = System

    name = FuzzyText(length=random.Random().randint(1, 100))
    description = FuzzyText(length=random.Random().randint(1, 600))


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = FuzzyText(length=random.Random().randint(1, 100))
    description = FuzzyText(length=random.Random().randint(1, 600))

    @factory.post_generation
    def related_systems(self, create, extracted, **kwargs):
        if not create:
            all_systems = System.objects.all()
            r = random.Random()
            sample_systems = r.sample(list(all_systems), r.randint(0, len(all_systems)))
            for s in sample_systems:
                self.related_systems.add(s)

        if extracted:
            # A list of groups were passed in, use them
            for related_system in extracted:
                self.related_systems.add(related_system)


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    name = FuzzyText(length=random.Random().randint(1, 100))
    description = FuzzyText(length=random.Random().randint(1, 600))


class EntryFactory(DjangoModelFactory):
    week = FuzzyInteger(1, 52, 1)
    year = FuzzyInteger(1000, 9999, 1)
    hours = FuzzyDecimal(0.5, 50, 2)
    comment = FuzzyText(length=random.Random().randint(1, 5000))
    user = factory.LazyFunction(UserFactory)


class RegularEntryFactory(EntryFactory):
    class Meta:
        model = RegularEntry

    system = factory.LazyFunction(SystemFactory)
    project = factory.LazyFunction(ProjectFactory)
    task = factory.LazyFunction(TaskFactory)


class ActivityFactory(DjangoModelFactory):
    class Meta:
        model = Activity

    name = FuzzyText(length=random.Random().randint(1, 100))
    description = FuzzyText(length=random.Random().randint(1, 600))


class SpecialEntryFactory(EntryFactory):
    class Meta:
        model = SpecialEntry

    activity = factory.LazyFunction(ActivityFactory)

