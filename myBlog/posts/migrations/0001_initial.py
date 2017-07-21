# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('content', models.TextField()),
                ('slug', models.SlugField(default='aaa', unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
