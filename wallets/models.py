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

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from news.models import ArticlePage

class WalletsIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(blank=True)
    header_text = models.CharField(blank=True, max_length=255)
    
    content_panels = Page.content_panels + [
        FieldPanel('header_text'),
    ]
    
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(WalletsIndexPage, self).get_context(request)
        walletspages = WalletPage.objects.live().filter(sponsored=False)
        sponsoredwallets = WalletPage.objects.live().filter(sponsored=True).order_by('-first_published_at')
        
        page = request.GET.get('page')
        paginator = Paginator(walletspages, 12)  # Show 12 pages per page
        try:
            walletspages = paginator.page(page)
        except PageNotAnInteger:
            walletspages = paginator.page(1)
        except EmptyPage:
            walletspages = paginator.page(paginator.num_pages)
        
        context['walletspages'] = walletspages
        context['sponsoredwallets'] = sponsoredwallets
        
        return context
        
    @route('^coins/$', name='tag_archive')
    @route('^coins/(\w+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no wallets supporting {}'.format(tag.upper())
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
        return render(request, 'wallets/wallets_index_page.html', context)

    # def serve_preview(self, request, mode_name):
    #     # Needed for previews to work
    #     return self.serve(request)
        
    # def children(self):
    #     return self.get_children().specific().live()
        
    def get_posts(self, tag=None):
        posts = WalletPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag).order_by("-sponsored")
        return posts

    # Returns the list of Tags for all child posts of this BlogPage.
    # def get_child_tags(self):
    #     tags = []
    #     for post in self.get_posts():
    #         # Not tags.append() because we don't want a list of lists
    #         tags += post.get_tags
    #     tags = sorted(set(tags))
    #     return tags


# ... (Keep the definition of WalletsIndexPage)


class WalletPageTag(TaggedItemBase):
    content_object = ParentalKey('WalletPage', related_name='tagged_items')


# Keep the definition of WalletsIndexPage, and add:


class WalletPage(Page):
    date = models.DateField("Post date")
    about = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=WalletPageTag, blank=True, help_text='Supported coins')
    sponsored = models.BooleanField(default=False, blank=True)
    website = models.CharField(max_length=255, blank=True)
    safety = models.CharField(max_length=1, blank=True, help_text='1=VERY SAFE, 2=MODERATELY SAFE, 3=NOT SAFE')
    anonymity = models.CharField(max_length=255, blank=True)
    ease = models.CharField(max_length=255, blank=True)
    webwallet = models.BooleanField(default=False, blank=True)
    ios = models.BooleanField(default=False, blank=True)
    hardware = models.BooleanField(default=False, blank=True)
    android = models.BooleanField(default=False, blank=True)
    windows = models.BooleanField(default=False, blank=True)
    linux = models.BooleanField(default=False, blank=True)
    chrome = models.BooleanField(default=False, blank=True)
    macos = models.BooleanField(default=False, blank=True)
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
            FieldPanel('about'),
            FieldPanel('website'),
            FieldPanel('safety'),
            FieldPanel('anonymity'),
            FieldPanel('ease'),
        ], heading="Article information"),
        ImageChooserPanel('image'),
        MultiFieldPanel([
            FieldPanel('webwallet'),
            FieldPanel('ios'),
            FieldPanel('hardware'),
            FieldPanel('android'),
            FieldPanel('windows'),
            FieldPanel('linux'),
            FieldPanel('chrome'),
            FieldPanel('macos'),
        ], heading="Platforms"),
        FieldPanel('sponsored'),
    ]
    
    @property
    def get_tags(self):
        """
        Similar to the authors function above we're returning all the tags that
        are related to the blog post into a list we can access on the template.
        We're additionally adding a URL to access BlogPage objects with that tag
        """
        tags = self.tags.all()
        return tags
        
    # Specifies parent to BlogPage as being BlogIndexPages
    parent_page_types = ['WalletsIndexPage']

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []
    
    def children(self):
        return self.get_children().specific().live().order_by('-first_published_at')
    
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(WalletPage, self).get_context(request)
        walletspages = WalletPage.objects.live().order_by('-first_published_at')
        newspages = ArticlePage.objects.live().filter(press_release=False).order_by('-first_published_at')
        context['newspages'] = newspages
        context['walletspages'] = walletspages
        return context