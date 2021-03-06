# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-07 09:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20171121_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aqi',
            name='of_date',
            field=models.DateField(default=datetime.datetime(2017, 12, 7, 9, 9, 13, 943461, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='data',
            name='co',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='measuring_date',
            field=models.DateField(default=datetime.datetime(2017, 12, 7, 9, 9, 13, 942461, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='data',
            name='nitrogen',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='ozone',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='pmten',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='sulphur',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='co',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='nitrogen',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='ozone',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='pmten',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='sulphur',
            field=models.FloatField(null=True),
        ),
    ]
