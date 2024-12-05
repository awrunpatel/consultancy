from django.urls import path
from .views import *


app_name = "events"

urlpatterns = [
    path("", EventsListView.as_view(), name="events"),
    path("create/", EventsView.as_view(), name="events_create"),
    path('update/<int:pk>/', EventsView.as_view(), name='events_update'),
    path("enquiry/json/", EventsAjaxView.as_view(), name="eventsajax"),
]
