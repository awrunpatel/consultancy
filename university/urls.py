from django.urls import path
from . import views

app_name = 'universities'

urlpatterns = [
    path('', views.UniversityListView.as_view(), name='university_list'),
    path('create/', views.UniversityView.as_view(), name='create_university'),
    path('update/<int:pk>/', views.UniversityView.as_view(), name='update_university'),
    path('ajax/', views.UniversityAjax.as_view(), name='university_ajax'),

    path('course/create/', views.UniversityCourseView.as_view(), name='create_university_course'),
    path('course/update/<int:pk>/', views.UniversityCourseView.as_view(), name='update_university_course'),
    path('course/', views.UniversityCourseListView.as_view(), name='university_course_list'),
    path('course/ajax/', views.UniversityCourseAjax.as_view(), name='university_course_ajax'),

    path('intake/create/', views.IntakeView.as_view(), name='create_intake'),
    path('intake/update/<int:pk>/', views.IntakeView.as_view(), name='update_intake'),
    path('intake/', views.IntakeListView.as_view(), name='intake_list'),
    path('intake/ajax/', views.IntakeAjax.as_view(), name='intake_ajax'),
]
