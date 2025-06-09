from django.urls import path
from .views import review_create, review_list

app_name = 'reviews'
urlpatterns = [
    path('', review_list, name='review_list'),
    path('add/<int:product_pk>/', review_create, name='review_create'),
]