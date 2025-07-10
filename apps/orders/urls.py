from django.urls import path
from .views import order_create, order_detail

app_name = 'orders'
urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('<int:pk>/', order_detail, name='order_detail'),
]
