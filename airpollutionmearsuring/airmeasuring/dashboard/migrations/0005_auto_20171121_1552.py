# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-21 08:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('manage_devices', '0004_auto_20171121_1552'),
        ('dashboard', '0004_auto_20170918_0356'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rawdata',
            options={'get_latest_by': 'measuring_date'},
        ),
        migrations.AddField(
            model_name='data',
            name='node',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manage_devices.Node'),
        ),
        migrations.AlterField(
            model_name='data',
            name='measuring_date',
            field=models.DateField(default=datetime.datetime(2017, 11, 21, 8, 52, 41, 348721, tzinfo=utc)),
        ),
    ]
