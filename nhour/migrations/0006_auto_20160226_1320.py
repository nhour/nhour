# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-26 13:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nhour', '0005_auto_20160226_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='nhour.Project'),
        ),
    ]
