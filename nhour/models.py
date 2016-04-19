from __future__ import unicode_literals
import re
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CharField, TextField, DateField, DateTimeField, ForeignKey, DecimalField, EmailField, \
    ManyToManyField
from django.db.models.fields import IntegerField

WEEK_FORMAT = r'^[0-9]{2}-[0-9]{4}$'


class System(models.Model):
    name = CharField(max_length=100)
    description = TextField(max_length=600, blank=True)

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


class Entry(models.Model):
    week = IntegerField(validators=[MaxValueValidator(52),
                                    MinValueValidator(1)])
    year = IntegerField(validators=[MaxValueValidator(9999),
                                    MinValueValidator(1000)])
    system = ForeignKey(
        'System',
        on_delete=models.PROTECT
    )
    project = ForeignKey(
        'Project',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    task = ForeignKey(
        'Task',
        on_delete=models.PROTECT
    )
    hours = DecimalField(decimal_places=1, max_digits=100, validators=[MaxValueValidator(100),
                                                                       MinValueValidator(0)])
    user = IntegerField()
    comment = TextField(max_length=5000, blank=True, null=True)
