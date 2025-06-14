from django.urls import path
from .views import order_create, order_detail, payment_callback, paystack_webhook

app_name = 'orders'

urlpatterns = [
    path('create/',    order_create,       name='order_create'),
    path('<int:pk>/',  order_detail,       name='order_detail'),
    path('callback/',  payment_callback,   name='payment_callback'),
    path('webhook/', paystack_webhook, name='paystack_webhook'),
]