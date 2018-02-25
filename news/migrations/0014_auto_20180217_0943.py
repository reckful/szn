# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-17 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_articlepage_preview_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='coin_four_link',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='coin_one_link',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='coin_three_link',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='coin_two_link',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]