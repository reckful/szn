# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-11 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0017_auto_20180219_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='preview_text',
            field=models.CharField(blank=True, max_length=140),
        ),
    ]
