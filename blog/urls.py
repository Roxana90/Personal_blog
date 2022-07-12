from . import views
from django.urls import path


app_name = 'blog'
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('contact/', views.contact_page, name='contact'),
    path('post/<slug:slug>/like', views.like_post, name='like'),
]
