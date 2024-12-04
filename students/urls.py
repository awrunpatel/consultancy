from django.urls import path
from .views import *

app_name = "students"

urlpatterns = [
    path('add/', StudentView.as_view(), name='add'),
    path('edit/<id>/', StudentEditView.as_view(), name='edit'),
    path('', StudentList.as_view(), name='list'),
    path('students/ajax/', StudentAjax.as_view(), name='ajax'),

    path('student/<pk>/educational/history/json/', EducationalHistoryJson.as_view(), name="educational_history_json"),
]