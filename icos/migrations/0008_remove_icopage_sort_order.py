# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-13 21:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icos', '0007_icopage_sort_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='icopage',
            name='sort_order',
        ),
    ]
