from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', views.BlogView.as_view(), name='blog_update'),
    path('blog/new/', views.BlogView.as_view(), name='blog_create'),
    path('ajax/', views.BlogAjaxView.as_view(), name='blog_ajax'),
]
