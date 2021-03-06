# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-21 16:18
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manage_devices', '0010_auto_20171221_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='node',
            name='last_connect',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 21, 16, 18, 18, 211946, tzinfo=utc)),
        ),
    ]
