# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-21 15:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('manage_devices', '0008_auto_20171218_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='last_connect',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 21, 15, 47, 36, 612613, tzinfo=utc)),
        ),
    ]
