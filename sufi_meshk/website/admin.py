from django.contrib import admin
from django.db import models
from.models import SocialMediaLink, GroupMember, FAQ, Update, Event, EventImage, Category, Tag, BlogPost, Author
from django_ckeditor_5.widgets import CKEditor5Widget
from modeltranslation.admin import TranslationAdmin

class GroupMemberAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget},
    }

admin.site.register(SocialMediaLink)
admin.site.register(GroupMember, GroupMemberAdmin)
admin.site.register(FAQ)
admin.site.register(Update)


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1  # Number of empty forms to display

class EventAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')},
    }
    inlines = [EventImageInline]
    list_display = ('event_name', 'date', 'place') 
    search_fields = ('event_name', 'description', 'place')
    list_filter = ('date',)  

admin.site.register(Event, EventAdmin)

admin.site.register(Category)
admin.site.register(Tag)

class BlogPostAdmin(TranslationAdmin):  # TranslationAdmin kullanıyoruz
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')},
    }
    list_display = ('title', 'author', 'status', 'create_date')
    search_fields = ('title', 'content')
    list_filter = ('status', 'create_date')

admin.site.register(BlogPost, BlogPostAdmin)

admin.site.register(Author)
