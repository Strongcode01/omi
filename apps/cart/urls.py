from django.urls import path
from .views import cart_detail, cart_add, cart_remove, cart_update, cart_deduct

app_name = 'cart'
urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:pk>/', cart_add, name='cart_add'),
    path('remove/<int:pk>/', cart_remove, name='cart_remove'),
    path('update/<int:pk>/', cart_update, name='cart_update'),
    path('deduct/<int:pk>/', cart_deduct, name='cart_deduct'),
]