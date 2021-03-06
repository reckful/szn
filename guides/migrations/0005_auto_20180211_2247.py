# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-11 22:47
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0004_guidepage_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidesindexpage',
            name='gettingstarted_count',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='guidesindexpage',
            name='mining_count',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='guidesindexpage',
            name='miscellaneous',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='guidesindexpage',
            name='safety_count',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='guidesindexpage',
            name='trading_count',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='guidesindexpage',
            name='utilising_count',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
    ]
