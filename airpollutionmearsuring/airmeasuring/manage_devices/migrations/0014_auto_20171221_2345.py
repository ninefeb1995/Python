# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-21 16:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('manage_devices', '0013_auto_20171221_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='area_name', to='dashboard.Area'),
        ),
        migrations.AlterField(
            model_name='node',
            name='last_connect',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 21, 16, 45, 21, 144772, tzinfo=utc)),
        ),
    ]
