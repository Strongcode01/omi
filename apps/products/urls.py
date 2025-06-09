from django.urls import path
from .views import product_list, product_detail, product_create
from apps.cart.views import cart_add

app_name = 'products'
urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', product_create, name='product_create'),
    path('<int:pk>/', product_detail, name='product_detail'),
    path('add/<int:pk>/', cart_add, name='cart_add'),
]
