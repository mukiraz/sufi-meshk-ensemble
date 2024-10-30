from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import User

class SocialMediaLink(models.Model):
    platform_name = models.CharField(max_length=50, help_text="Name of the social media platform")
    url = models.URLField(max_length=200, help_text="URL to the social media profile")
    icon_class = models.CharField(max_length=100, help_text="FontAwesome icon class for the platform")
    author_specific = models.BooleanField(default=False, help_text="True if this link is specific to an author")

    def __str__(self):
        return self.platform_name
    
class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    position = models.CharField(max_length=100, help_text="Author's position (e.g., Editor)")
    short_description = models.CharField(max_length=300, help_text="A short bio of the author")
    photo = models.ImageField(upload_to='authors/', help_text="Photo of the author", blank=True, null=True)
    social_media_links = models.ManyToManyField(SocialMediaLink, blank=True, help_text="Author's social media links")

    def __str__(self):
        return f"{self.name} {self.surname}"

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

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True, help_text='SEO title, maximum 200 characters')
    meta_description = models.CharField(max_length=160, blank=True, help_text='SEO meta description, maximum 160 characters')
    meta_keywords = models.CharField(max_length=255, blank=True, help_text='Comma-separated keywords for SEO')
    meta_author = models.CharField(max_length=100, blank=True, help_text='Author name for SEO (optional)')
    
    # Open Graph and Twitter fields
    og_title = models.CharField(max_length=200, blank=True, help_text='Open Graph title for social media')
    og_description = models.CharField(max_length=200, blank=True, help_text='Open Graph description for social media')
    og_image = models.ImageField(upload_to='og_images/', blank=True, null=True)
    twitter_card_type = models.CharField(max_length=20, blank=True, default='summary_large_image', help_text='Type of Twitter card (summary, summary_large_image)')
 
    short_description = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, help_text="Author of the blog post")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    # ForeignKey for Category and ManyToMany for Tags
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    view_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        # Automate meta tags if not provided
        if not self.meta_title:
            self.meta_title = self.title[:200]
        if not self.meta_description:
            self.meta_description = self.content[:160]
        if not self.meta_keywords:
            self.meta_keywords = ', '.join(self.title.lower().split())
        
        # Set meta_author if not provided
        if not self.meta_author and self.author:
            self.meta_author = f"{self.author.name} {self.author.surname}"
        
        if not self.og_title:
            self.og_title = self.meta_title
        if not self.og_description:
            self.og_description = self.meta_description
        if not self.og_image and self.featured_image:
            self.og_image = self.featured_image
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

