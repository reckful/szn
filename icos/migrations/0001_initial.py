# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-11 15:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.contrib.wagtailroutablepage.models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='IcoPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('date', models.DateField(verbose_name='Post date')),
                ('date_active', models.DateField(verbose_name='Date active')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('website', models.CharField(blank=True, max_length=255)),
                ('whitepaper', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='IcoPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='icos.IcoPage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='icos_icopagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IcosIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.AddField(
            model_name='icopage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='icos.IcoPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]