"""
URL configuration for sufi_meshk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.views.generic import TemplateView
from website.sitemaps import BlogPostSitemap, CategorySitemap, TagSitemap, EventSitemap, StaticViewSitemap

sitemaps = {
    'blogposts': BlogPostSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap,
    'events': EventSitemap,
    'static':StaticViewSitemap
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # Include the set_language URL
    path("ckeditor5/", include('django_ckeditor_5.urls')),  # CKEditor 5 ana yolları
    path("ckeditor/upload/", include("ckeditor_uploader.urls")),  # CKEditor yükleme yolları
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', include('website.urls')),  # Include app's URLs
    prefix_default_language=True,  # Optional: adjust based on whether you want a prefix for default language
)


