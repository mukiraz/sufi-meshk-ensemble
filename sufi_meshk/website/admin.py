from django.contrib import admin
from django.db import models
from.models import SocialMediaLink, GroupMember, FAQ, Update, Event, EventImage
from django_ckeditor_5.widgets import CKEditor5Widget

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
    inlines = [EventImageInline]
    list_display = ('event_name', 'date', 'place', 'status')
    search_fields = ('event_name', 'description', 'place')
    list_filter = ('status', 'date')

admin.site.register(Event, EventAdmin)
