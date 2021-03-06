# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-15 03:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('node_identification', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('is_available', models.BooleanField(default=False)),
                ('longitude', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Area')),
                ('gateway_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_devices.Node')),
            ],
        ),
    ]
