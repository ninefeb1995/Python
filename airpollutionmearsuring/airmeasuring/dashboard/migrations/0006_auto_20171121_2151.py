# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-21 14:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('manage_devices', '0005_auto_20171121_2151'),
        ('dashboard', '0005_auto_20171121_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='AQI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('of_date', models.DateField(default=datetime.datetime(2017, 11, 21, 14, 50, 39, 498417, tzinfo=utc))),
                ('node', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manage_devices.Node')),
            ],
        ),
        migrations.RenameField(
            model_name='data',
            old_name='oxi',
            new_name='nitrogen',
        ),
        migrations.RenameField(
            model_name='rawdata',
            old_name='oxi',
            new_name='nitrogen',
        ),
        migrations.AddField(
            model_name='data',
            name='ozone',
            field=models.FloatField(default=22.3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='pmten',
            field=models.FloatField(default=22.5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='sulphur',
            field=models.FloatField(default=1.2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rawdata',
            name='ozone',
            field=models.FloatField(default=2.4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rawdata',
            name='pmten',
            field=models.FloatField(default=2.4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rawdata',
            name='sulphur',
            field=models.FloatField(default=1.3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='data',
            name='measuring_date',
            field=models.DateField(default=datetime.datetime(2017, 11, 21, 14, 50, 39, 496417, tzinfo=utc)),
        ),
    ]
