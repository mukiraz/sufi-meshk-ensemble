# your_app/urls.py
from django.urls import path
from . import views
from .views import BlogListByCategoryView, BlogListByTagView, BlogSearchView, BlogDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us', views.about_us, name="about_us"),
    path('group-member/<int:id>/', views.group_member_detail, name='group-member-detail'),
    path('media', views.gallery_view, name='media'),
    path('updates/', views.updates_view, name='updates'),
    path('events/future/', views.future_events_view, name='future_events'),
    path('events/past/', views.past_events_view, name='past_events'),
    path('events/<int:event_id>/', views.event_detail_view, name='event_detail'),
    path('category/<slug:slug>/', BlogListByCategoryView.as_view(), name='blog_list_by_category'),
    path('tag/<slug:slug>/', BlogListByTagView.as_view(), name='blog_list_by_tag'),
    path('search/', BlogSearchView.as_view(), name='blog_search'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail')
]