from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class SocialMediaLink(models.Model):
    platform_name = models.CharField(max_length=50, help_text="Name of the social media platform")
    url = models.URLField(max_length=200, help_text="URL to the social media profile")
    icon_class = models.CharField(max_length=100, help_text="FontAwesome icon class for the platform")

    def __str__(self):
        return self.platform_name
    

class GroupMember(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    instrument_duty = models.CharField(max_length=100, help_text="The member's main role or instrument")
    short_description = models.CharField(max_length=600, help_text="A short description of the member (max 600 characters)")
    description = models.TextField()
    photo = models.ImageField(upload_to='group_members/', help_text="Photo of the member")
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.name} {self.surname}"
    
class FAQ(models.Model):
    question = models.CharField(max_length=400)
    answer = models.TextField()

    def __str__(self):
        return self.question

class Update(models.Model):
    featured_image = models.ImageField(upload_to='updates/')
    title = models.CharField(max_length=400)
    short_description = models.TextField()
    external_link = models.URLField(max_length=400)
    release_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    featured_image = models.ImageField(upload_to='events/featured/')
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    place = models.CharField(max_length=255)
    maps_iframe = models.TextField(null=True, blank=True)
    ticket_link = models.URLField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    organizer = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('upcoming', _('Upcoming')),
            ('ongoing', _('Ongoing')),
            ('past', _('Past'))
        ],
        default='upcoming'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contact_info = models.TextField(null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    published = models.BooleanField(default=True)
    tags = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.event_name

    def save(self, *args, **kwargs):
        self.set_status()
        super(Event, self).save(*args, **kwargs)

    def set_status(self):
        """Determine and set the status of the event based on the current date."""
        now = timezone.now().date()
        if self.end_date and self.end_date < now:
            self.status = 'past'
        elif self.date == now:
            self.status = 'ongoing'
        elif self.date > now:
            self.status = 'upcoming'


class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/images/')
    caption = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Image for {self.event.event_name}"

