# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import RawHTMLBlock
from wagtail.wagtailcore.blocks import BlockQuoteBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore.models import Page
from django.shortcuts import redirect, render
from django.contrib import messages


class GuidesIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(blank=True)
    gettingstarted_count = models.CharField(blank=True, max_length=15)
    safety_count = models.CharField(blank=True, max_length=15)
    trading_count = models.CharField(blank=True, max_length=15)
    mining_count = models.CharField(blank=True, max_length=15)
    utilising_count = models.CharField(blank=True, max_length=15)
    miscellaneous = models.CharField(blank=True, max_length=15)
    
    content_panels = Page.content_panels + [
       FieldPanel('gettingstarted_count'),
       FieldPanel('safety_count'),
       FieldPanel('trading_count'),
       FieldPanel('mining_count'),
       FieldPanel('utilising_count'),
       FieldPanel('miscellaneous'),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(GuidesIndexPage, self).get_context(request)
        guidespages = self.get_children().live().order_by('first_published_at')
        context['guidespages'] = guidespages
        return context
        
    @route('^category/$', name='tag_archive')
    @route('^category/(\w+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no guides mentioning the coin"{}"'.format(tag).upper()
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
        return render(request, 'guides/guides_index_page.html', context)

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)
        
    def children(self):
        return self.get_children().specific().live()
        
    def get_posts(self, tag=None):
        posts = GuidePage.objects.live().descendant_of(self)
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


# ... (Keep the definition of GuidesIndexPage)


class GuidePageTag(TaggedItemBase):
    content_object = ParentalKey('GuidePage', related_name='tagged_items')


# Keep the definition of GuidesIndexPage, and add:


class GuidePage(Page):
    date = models.DateField("Post date")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    tags = ClusterTaggableManager(through=GuidePageTag, blank=True)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('rawhtml', RawHTMLBlock()),
        ('quote', BlockQuoteBlock()),
        ('embed', EmbedBlock()),
    ])
    length = models.CharField("Length of guide", blank=True, max_length=20)
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
       FieldPanel('date'),
       StreamFieldPanel('body'),
       FieldPanel('tags'),
       ImageChooserPanel('image'),
       FieldPanel('length'),
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
    parent_page_types = ['GuidesIndexPage']

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []
    
    def children(self):
        return self.get_children().specific().live().order_by('-first_published_at')
    
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(GuidePage, self).get_context(request)
        guidespages = self.get_parent().get_children().live().order_by('-first_published_at')[:4]
        context['guidespages'] = guidespages
        return context