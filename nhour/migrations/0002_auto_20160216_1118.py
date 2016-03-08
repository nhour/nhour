# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-16 11:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nhour', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nhour.Project'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nhour.System'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nhour.Task'),
        ),
    ]
