from django.urls import path
from .views import home, newsletter, ContactPageView, ServicesPageView, send_message, contact_us, contact_submit

app_name = 'pages'
urlpatterns = [
    path('', home, name='home'),
    # path('contact/', ContactPageView.as_view(), name='contact'),
    path('contact/', contact_us, name='contact_us'),
    path('contact_submit/', contact_submit, name='contact_submit'),
    path('services/', ServicesPageView.as_view(), name='services'),
    path('newsletter/', newsletter, name='newsletter'),
    path('send_message/', send_message, name='send_message'),
]
