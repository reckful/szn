# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-13 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icos', '0005_auto_20180213_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icopage',
            name='date_end',
            field=models.DateTimeField(blank=True, verbose_name='Date end'),
        ),
    ]
