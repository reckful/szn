# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-13 20:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_articlepage_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsindexpage',
            name='header_text',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
