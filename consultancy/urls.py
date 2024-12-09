"""
URL configuration for consultancy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generic/', include("dashboard.generic_urls", namespace="generic")),
    path('',include('dashboard.urls'), name='dashboard'),
    path('',include('userauth.urls'), name='userauth'),
    path('',include('filehub.urls'), name='filehub'),
    path('users/',include('users.urls'), name='users'),
    path('students/',include('students.urls'), name='students'),
    path('courses/',include('courses.urls'), name='courses'),
    path('university/',include('university.urls'), name='university'),
    path('events/',include('events.urls'), name='events'),
    path('blogs/',include('blogs.urls'), name='blogs'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
