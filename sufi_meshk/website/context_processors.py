from .models import Category, SocialMediaLink, BlogPost

def common_page_objects(request):
    return {
        'categories': Category.objects.all(),
        'social_links': SocialMediaLink.objects.all(),
        'latest_blogs': BlogPost.objects.filter(status='published').order_by('-create_date')[:3],
    }