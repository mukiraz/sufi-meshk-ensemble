import os
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import SocialMediaLink, GroupMember, FAQ, Update, Event


# Create your views here.
class PageObjects():
    def __init__(self):
        self.objects = dict()

    def get_header_objects(self):
        pass

    def get_future_events(self):
        now = timezone.now().date()
        return Event.objects.filter(date__gte=now).order_by('date')


    def get_footer_objects(self):
        social_links = SocialMediaLink.objects.all()
        self.objects['social_links'] = social_links

    def get_index_page_objects(self):
        faqs = FAQ.objects.all()
        self.get_footer_objects()
        self.objects["faqs"] = faqs
        self.objects["title"] = _('Home')
        self.objects["future_events"] = self.get_future_events()
        return self.objects
    
    def get_about_us_objects(self):
        self.get_footer_objects()
        group_members = GroupMember.objects.all()
        self.objects['group_members'] = group_members
        self.objects["title"] = _('About Us')
        return self.objects
    
    def get_group_member(self, id):
        self.get_footer_objects()
        member = get_object_or_404(GroupMember, id=id)
        self.objects['member'] = member
        self.objects["title"] = f"{member.name} {member.surname}"
        return self.objects
    
    def get_gallery_view_objects(self):
        media_root = os.path.join(settings.MEDIA_ROOT, 'gallery')
        images = [f'/media//gallery/{file}' for file in os.listdir(media_root) if file.endswith(('jpg', 'jpeg', 'png', 'gif'))]
        print(images)
        self.objects["images"] = images
        self.objects["title"] = _("Media")
        return self.objects

    def get_updates_view_objects(self):
        updates = Update.objects.filter(is_active=True)
        self.objects["updates"] = updates
        self.objects["title"] = _("Updates")
        return self.objects

    def get_future_events_view(self):
        # Filter events that are upcoming or ongoing
        self.objects["future_events"] = self.get_future_events()
        self.objects["title"] = _("Future Events")
        return self.objects

    def get_past_events_view(self):
        # Filter events that are past
        now = timezone.now().date()
        self.objects["past_events"] = Event.objects.filter(date__lt=now).order_by('-date')
        self.objects["title"] = _("Old Events")
        return self.objects

    def get_event_detail_objects(self, event_id):
        event = get_object_or_404(Event, id=event_id)
        now = timezone.now().date()
        # Fetch future events
        future_events = Event.objects.filter(date__gte=now).exclude(id=event.id).order_by('date')
        # Fetch last 4 past events
        past_events = Event.objects.filter(date__lt=now).exclude(id=event.id).order_by('-date')[:4]
        self.objects['event'] = event
        self.objects['future_events'] = future_events
        self.objects['past_events'] = past_events
        self.objects["title"] = event.event_name
        return self.objects


def index(request):
    page_objects = PageObjects().get_index_page_objects()
    return render(request, 'index.html', page_objects)

def about_us(request):
    page_objects = PageObjects().get_about_us_objects()
    return render(request, 'about-us.html', page_objects)

def group_member_detail(request, id):
    page_objects = PageObjects().get_group_member(id)
    return render(request, 'group-member.html', page_objects)

def gallery_view(request):
    page_objects = PageObjects().get_gallery_view_objects()
    return render(request, 'media.html', page_objects)

def updates_view(request):
    page_objects = PageObjects().get_updates_view_objects()
    return render(request, 'updates.html', page_objects)


def future_events_view(request):
    page_objects = PageObjects().get_future_events_view()
    return render(request, 'future_events.html', page_objects)

def past_events_view(request):
    page_objects = PageObjects().get_past_events_view()
    return render(request, 'past_events.html', page_objects)


def event_detail_view(request, event_id):
    page_objects = PageObjects().get_event_detail_objects(event_id)
    return render(request, 'event-detail.html', page_objects)

