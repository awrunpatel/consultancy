from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('add/', views.CourseView.as_view(), name='add_course'),
    path('edit/<int:pk>/', views.CourseView.as_view(), name='update_course'),
    path('', views.CourseListView.as_view(), name='course_list'),
    path('ajax/course/', views.CourseAjax.as_view(), name='course_ajax'),
]
