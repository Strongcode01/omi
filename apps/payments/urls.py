from django.urls import path
from .views import make_payment, verify_payment, webhook

app_name = 'payments'
urlpatterns = [
    path('pay/<str:ref>/',    make_payment,  name='make_payment'),
    path('verify/<str:ref>/', verify_payment, name='verify_payment'),
    path('webhook/',          webhook,        name='webhook'),
]