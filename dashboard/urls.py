from django.urls import path
from .views import *


app_name = "dashboard"

urlpatterns = [
    path('',DashboardView.as_view(), name='index'),
    path("filemanager/", FileManagerView.as_view(), name="filemanager"),
    path("settings/", SettingsView.as_view(), name="settings"),
    
    
    path("delete/", DeleteView.as_view(), name="delete"),
    path("delete/final/", DeleteFinalView.as_view(), name="deletefinal"),


]