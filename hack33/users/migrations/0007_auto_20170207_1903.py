# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 19:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_hour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hour',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Classroom'),
        ),
    ]
