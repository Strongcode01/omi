from django.urls import path
from .views import request_list, request_create, request_detail

app_name = 'diagnostics'
urlpatterns = [
    path('', request_list, name='request_list'),
    path('new/', request_create, name='request_create'),
    path('<int:pk>/', request_detail, name='request_detail'),
]