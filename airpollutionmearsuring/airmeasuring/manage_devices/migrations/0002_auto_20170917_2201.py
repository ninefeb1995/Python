# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-17 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_devices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='latitude',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='longitude',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
