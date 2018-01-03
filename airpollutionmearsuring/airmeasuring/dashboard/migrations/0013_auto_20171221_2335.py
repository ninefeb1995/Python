# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-21 16:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20171221_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aqi',
            name='of_date',
            field=models.DateField(default=datetime.datetime(2017, 12, 21, 16, 35, 4, 22475, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='data',
            name='measuring_date',
            field=models.DateField(default=datetime.datetime(2017, 12, 21, 16, 35, 4, 20475, tzinfo=utc)),
        ),
    ]