# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-11 17:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('icos', '0003_auto_20180211_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='icopage',
            name='date_active',
        ),
        migrations.AddField(
            model_name='icopage',
            name='date_end',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Date end'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='icopage',
            name='date_start',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Date start'),
            preserve_default=False,
        ),
    ]
