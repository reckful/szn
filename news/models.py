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

from django.db.models import prefetch_related_objects

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore.models import Page
from django.shortcuts import redirect, render
from django.contrib import messages


class NewsIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(blank=True)
    header_text = models.CharField(blank=True, max_length=255)
    
    content_panels = Page.content_panels + [
        FieldPanel('header_text'),
    ]
    
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(NewsIndexPage, self).get_context(request)
        newspages = ArticlePage.objects.live().filter(press_release=False).order_by('-first_published_at')
        pressreleases = ArticlePage.objects.live().filter(press_release=True).order_by('-first_published_at')
        context['newspages'] = newspages
        context['pressreleases'] = pressreleases
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
        return render(request, 'news/news_index_page.html', context)
    
    @route('^press/$', name='press_archive')
    @route('^press/(\w+)/$', name='press_archive')   
    def press_archive(self, request, tag=None):

        releases = ArticlePage.objects.live().filter(press_release=True).order_by('-first_published_at')
        context = {
            'releases': releases,
        }
        return render(request, 'news/news_index_page.html', context)

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)
        
    def children(self):
        return self.get_children().specific().live()
        
    def get_posts(self, tag=None):
        posts = ArticlePage.objects.live().descendant_of(self)
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


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey('ArticlePage', related_name='tagged_items')


# Keep the definition of NewsIndexPage, and add:


class ArticlePage(Page):
    date = models.DateField("Post date")
    preview_text = RichTextField(blank=True, max_length=255)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('rawhtml', RawHTMLBlock()),
        ('quote', BlockQuoteBlock()),
        ('embed', EmbedBlock()),
    ])
    coin_one = models.CharField(max_length=250, blank=True)
    coin_two = models.CharField(max_length=250, blank=True)
    coin_three = models.CharField(max_length=250, blank=True)
    coin_four = models.CharField(max_length=250, blank=True)
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    featured = models.BooleanField(default=False, blank=True)
    author = RichTextField(blank=True)
    sponsored = models.BooleanField(default=False, blank=True)
    press_release = models.BooleanField(default=False, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('featured'),
            FieldPanel('sponsored'),
            FieldPanel('press_release'),
            FieldPanel('author'),
        ], heading="Article information"),
        ImageChooserPanel('image'),
        FieldPanel('preview_text'),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('coin_one'),
            FieldPanel('coin_two'),
            FieldPanel('coin_three'),
            FieldPanel('coin_four'),
        ], heading="Coins mentioned"),
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
    parent_page_types = ['NewsIndexPage']

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []
    
    def children(self):
        return self.get_children().specific().live().order_by('-first_published_at')
    
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(ArticlePage, self).get_context(request)
        newspages = ArticlePage.objects.live().filter(press_release=False).order_by('-first_published_at')
        context['newspages'] = newspages
        return context