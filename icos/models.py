# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore.models import Page
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone

from news.models import ArticlePage

class IcosIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(IcosIndexPage, self).get_context(request)
        icopages = IcoPage.objects.live().filter(featured_ico=False).order_by('date_end')
        featuredicos = IcoPage.objects.live().filter(featured_ico=True).order_by('date_end')
        now = timezone.now()
        context['icopages'] = icopages
        context['featuredicos'] = featuredicos
        context['now'] = now
        return context
        
    @route('^tags/$', name='tag_archive')
    @route('^tags/(\w+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no articles mentioning the coin"{}"'.format(tag.upper())
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        tags = []
        for post in self.get_posts():
            tags += post.get_tags
            tags = sorted(set(tags))
        context = {
            'tag': tag,
            'posts': posts,
            'tags': tags
        }
        return render(request, 'icos/icos_index_page.html', context)

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)
        
    def children(self):
        return self.get_children().specific().live()
        
    def get_posts(self, tag=None):
        posts = IcoPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    # Returns the list of Tags for all child posts of this BlogPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags


# ... (Keep the definition of NewsIndexPage)


class IcoPageTag(TaggedItemBase):
    content_object = ParentalKey('IcoPage', related_name='tagged_items')


# Keep the definition of NewsIndexPage, and add:


class IcoPage(Page):
    date = models.DateField("Post date")
    date_start = models.DateTimeField("Date start", blank=True)
    date_end = models.DateTimeField("Date end", blank=True)
    pre_ico = models.BooleanField(default=False, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    description = models.CharField(blank=True, max_length=255)
    about = RichTextField(blank=True)
    website = models.CharField(blank=True, max_length=255)
    whitepaper = models.CharField(blank=True, max_length=255)
    tags = ClusterTaggableManager(through=IcoPageTag, blank=True)
    featured_ico = models.BooleanField(blank=True)
    reddit = models.CharField(blank=True, max_length=255)
    twitter = models.CharField(blank=True, max_length=255)
    facebook = models.CharField(blank=True, max_length=255)
    linkedin = models.CharField(blank=True, max_length=255)
    instagram = models.CharField(blank=True, max_length=255)
    telegram = models.CharField(blank=True, max_length=255)
    search_fields = Page.search_fields + [
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('date_start'),
            FieldPanel('date_end'),
            ImageChooserPanel('image'),
            FieldPanel('pre_ico'),
            FieldPanel('description'),
            FieldPanel('about'),
            FieldPanel('whitepaper'),
            FieldPanel('website'),
            FieldPanel('featured_ico'),
        ], heading="ICO information"),
        MultiFieldPanel([
            FieldPanel('reddit'),
            FieldPanel('twitter'),
            FieldPanel('facebook'),
            FieldPanel('linkedin'),
            FieldPanel('instagram'),
            FieldPanel('telegram'),
        ], heading="ICO Links"),
    ]
    
    @property
    def get_tags(self):
        """
        Similar to the authors function above we're returning all the tags that
        are related to the blog post into a list we can access on the template.
        We're additionally adding a URL to access BlogPage objects with that tag
        """
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/'+'/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tags',
                tag.slug
            ])
        return tags

    # Specifies parent to BlogPage as being BlogIndexPages
    parent_page_types = ['IcosIndexPage']

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []
    
    def children(self):
        return self.get_children().specific().live().order_by('-first_published_at')
    
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(IcoPage, self).get_context(request)
        newspages = ArticlePage.objects.live().filter(press_release=False).order_by('-first_published_at')
        icopages = self.get_parent().get_children().live().order_by('-first_published_at')[:4]
        context['newspages'] = newspages
        context['icopages'] = icopages
        return context