from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path('list/', UserListView.as_view(), name='user_list'),
    path('add/', UserView.as_view(), name='user_add'),
    path('edit/<int:pk>/', UserView.as_view(), name='user_edit'),
    path('ajax/', UserAjax.as_view(), name='user_ajax'),
]