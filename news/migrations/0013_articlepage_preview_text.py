# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-15 19:45
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0012_auto_20180215_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='preview_text',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, max_length=255),
        ),
    ]