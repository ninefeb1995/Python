# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-21 16:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('manage_devices', '0009_auto_20171221_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='last_connect',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 21, 16, 10, 24, 604857, tzinfo=utc)),
        ),
    ]
