import boto3, uuid
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import GroupMember, FAQ, Update, Event, BlogPost, Category, Tag
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


# Views

@csrf_exempt
def upload_image(request):
    print("deneme")
    if request.method == "POST" and request.FILES.get("upload"):
        upload = request.FILES["upload"]
        file_name = f'image_upload/{uuid.uuid4()}_{upload.name}'  # Benzersiz bir dosya adı oluştur
        file_path = default_storage.save(file_name, ContentFile(upload.read()))
        file_url = f"{settings.MEDIA_URL}{file_path}"
        return JsonResponse({"url": file_url})
    return JsonResponse({"error": "Dosya yüklenemedi"}, status=400)

def index(request):
    faqs = FAQ.objects.all()
    future_events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')
    context = {
        "faqs": faqs,
        "future_events": future_events,
        "title": _('Home')
    }
    return render(request, 'index.html', context)

def about_us(request):
    group_members = GroupMember.objects.all()
    context = {
        'group_members': group_members,
        "title": _('About Us')
    }
    return render(request, 'about-us.html', context)

def group_member_detail(request, slug):
    member = get_object_or_404(GroupMember, slug=slug)
    context = {
        'member': member,
        "title": f"{member.name} {member.surname}"
    }
    return render(request, 'group-member.html', context)

def gallery_view(request):
    s3 = boto3.client('s3')
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    prefix = 'media/gallery/'  # S3 bucket içindeki klasör yolu

    # 'gallery' klasöründeki tüm nesneleri listele
    result = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Görüntülerin URL'lerini oluştur
    images = []
    for content in result.get('Contents', []):
        key = content['Key']
        if key.endswith(('jpg', 'jpeg', 'png', 'gif')):
            url = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{key}'
            images.append(url)

    context = {
        "images": images,
        "title": _("Media")
    }
    return render(request, 'media.html', context)

def updates_view(request):
    updates = Update.objects.filter(is_active=True)
    context = {
        "updates": updates,
        "title": _("Updates")
    }
    return render(request, 'updates.html', context)

def future_events_view(request):
    future_events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')
    context = {
        "future_events": future_events,
        "title": _("Future Events")
    }
    return render(request, 'future_events.html', context)

def past_events_view(request):
    past_events = Event.objects.filter(date__lt=timezone.now().date()).order_by('-date')
    context = {
        "past_events": past_events,
        "title": _("Old Events")
    }
    return render(request, 'past_events.html', context)

def event_detail_view(request, slug):
    event = get_object_or_404(Event, slug=slug)
    current_datetime = timezone.now()
    today = current_datetime.date()
    now = current_datetime.time()
    
    future_events = Event.objects.filter(date__gte=today).exclude(slug=slug).order_by('date')
    past_events = Event.objects.filter(date__lt=today).exclude(slug=slug).order_by('-date')[:4]
    
    context = {
        'event': event,
        'future_events': future_events,
        'past_events': past_events,
        'title': event.event_name,
        'today': today,   # Güncel tarih
        'now': now        # Güncel saat
    }
    return render(request, 'event-detail.html', context)

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)

class BlogListByCategoryView(ListView):
    model = BlogPost
    template_name = 'blog_list_by_category.html'
    context_object_name = 'blogs'
    paginate_by = 10  # Sayfa başına blog sayısını belirleyin (opsiyonel)

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=category_slug)
        return BlogPost.objects.filter(category=category, status='published').order_by('-create_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=category_slug)
        
        # İlgili kategoriye ait blogları hariç tutarak diğer blogları recent_blogs olarak ekleyelim
        context['category'] = category
        context['recent_blogs'] = BlogPost.objects.filter(status='published').exclude(category=category).order_by('-create_date')[:3]
        
        # Tüm etiketleri alarak tag cloud için context'e ekleyelim
        context['tags'] = Tag.objects.all()
        context['title'] = f"{category.name} { _('Blogs') }"  # Dinamik başlık
        return context
    
class BlogListByTagView(ListView):
    model = BlogPost
    template_name = 'blog_list_by_category.html'  # Aynı template'i kullanıyoruz
    context_object_name = 'blogs'
    paginate_by = 10  # Sayfa başına blog sayısını belirleyin (opsiyonel)

    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        tag = get_object_or_404(Tag, slug=tag_slug)
        return BlogPost.objects.filter(tags=tag, status='published').order_by('-create_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs['slug']
        tag = get_object_or_404(Tag, slug=tag_slug)
        
        # İlgili etikete ait blogları hariç tutarak diğer blogları recent_blogs olarak ekleyelim
        context['tag'] = tag
        context['recent_blogs'] = BlogPost.objects.filter(status='published').exclude(tags=tag).order_by('-create_date')[:3]
        
        # Tüm etiketleri alarak tag cloud için context'e ekleyelim
        context['tags'] = Tag.objects.all()
        context['title'] = f"{tag.name} { _('Tagged Blogs') }"  # Dinamik başlık
        
        return context

class BlogSearchView(ListView):
    model = BlogPost
    template_name = 'blog_list_by_category.html'  # Aynı template'i kullanıyoruz
    context_object_name = 'blogs'
    paginate_by = 10  # Sayfa başına sonuç sayısını belirleyin

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        if query:
            return BlogPost.objects.filter(
                (Q(title__icontains=query) | 
                Q(content__icontains=query) | 
                Q(short_description__icontains=query)) &
                Q(status='published')
            ).order_by('-create_date')
        else:
            return BlogPost.objects.none()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = self.request.GET.get('q')
        context['recent_blogs'] = BlogPost.objects.filter(status='published').order_by('-create_date')[:3]
        context['tags'] = Tag.objects.all()
        context['title'] = f"{ _('Search results for') } '{query}'" if query else _('Search Blogs')  # Dinamik başlık
        return context

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_detail.html'  # Aynı template'i kullanıyoruz
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_blogs'] = BlogPost.objects.filter(status='published').exclude(id=self.object.id).order_by('-create_date')[:3]
        context['tags'] = Tag.objects.all()
        context['title'] = self.object.title
        return context
    
