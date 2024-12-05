from django.urls import path
from .views import *


app_name = "dashboard"

urlpatterns = [
    path('',DashboardView.as_view(), name='index'),
    path("filemanager/", FileManagerView.as_view(), name="filemanager"),
    path("settings/", SettingsView.as_view(), name="settings"),

    path("enquiry/", EnquiryView.as_view(), name="enquiry"),
    path("enquiry/json/", EnquiryAjaxView.as_view(), name="enquiryajax"),

]
