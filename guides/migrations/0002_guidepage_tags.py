# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-11 19:38
from __future__ import unicode_literals

from django.db import migrations
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('guides', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidepage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='guides.GuidePageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
