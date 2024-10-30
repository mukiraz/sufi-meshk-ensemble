# website/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.conf import settings
from django.shortcuts import reverse
from .models import BlogPost, Category, Tag, Event

class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return f"{settings.SITE_URL}{reverse('blog_detail', args=[obj.slug])}"


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return f"{settings.SITE_URL}{reverse('blog_list_by_category', args=[obj.slug])}"


class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return f"{settings.SITE_URL}{reverse('blog_list_by_tag', args=[obj.slug])}"


class EventSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Event.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.date

    def location(self, obj):
        return f"{settings.SITE_URL}{reverse('event_detail', args=[obj.id])}"
    
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['index', 'about_us', 'media', 'updates']  # Önemli statik sayfaların URL isimleri

    def location(self, item):
        return f"{settings.SITE_URL}{reverse(item)}"


sitemaps = {
    'blogposts': BlogPostSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap,
    'events': EventSitemap,
    'static':StaticViewSitemap
}