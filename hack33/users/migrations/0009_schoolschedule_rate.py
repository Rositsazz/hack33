# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 22:51
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_schoolschedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolschedule',
            name='rate',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
    ]
