from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CharField, TextField, DateField, DateTimeField, ForeignKey, DecimalField, EmailField, \
    ManyToManyField, BooleanField
from django.db.models.fields import IntegerField


class System(models.Model):
    name = CharField(max_length=100)
    description = TextField(max_length=700, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = CharField(max_length=100)
    description = TextField(max_length=600, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = CharField(max_length=100)
    description = TextField(max_length=600, blank=True)
    related_systems = ManyToManyField(System)

    def __str__(self):
        return self.name


class CompletedWeek(models.Model):
    week = IntegerField(validators=[MaxValueValidator(53),
                                    MinValueValidator(1)])
    year = IntegerField(validators=[MaxValueValidator(9999),
                                    MinValueValidator(1000)])
    user = ForeignKey(User, on_delete=models.PROTECT)


class Entry(models.Model):
    week = IntegerField(validators=[MaxValueValidator(52),
                                    MinValueValidator(1)])
    year = IntegerField(validators=[MaxValueValidator(9999),
                                    MinValueValidator(1000)])
    hours = DecimalField(decimal_places=2,
                         max_digits=5,
                         validators=[MaxValueValidator(100),
                                     MinValueValidator(0)])
    user = ForeignKey(User, on_delete=models.PROTECT)
    comment = TextField(max_length=5000, blank=True, null=True)

    class Meta:
        ordering = ("-year", "-week")


class RegularEntry(Entry):
    system = ForeignKey('System', on_delete=models.PROTECT)
    project = ForeignKey(
        'Project', on_delete=models.PROTECT,
        null=True, blank=True)
    task = ForeignKey('Task', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Regular Entries"

    def __eq__(self, other):
        return isinstance(other, Entry) and other.id == self.id

    @staticmethod
    def get_entries_of_week(user, year, week):
        return RegularEntry.objects.filter(year=year, week=week, user=user)



class Activity(models.Model):
    name = CharField(max_length=100)
    description = TextField(max_length=600, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Activities"


class SpecialEntry(Entry):
    activity = ForeignKey('Activity', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Special Entries"

    @staticmethod
    def get_entries_of_week(user, year, week):
        return SpecialEntry.objects.filter(year=year, week=week, user=user)
