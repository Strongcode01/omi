from django.db import models
from django.conf import settings
from apps.products.models import Product
import secrets

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('P',  'Pending'),
        ('PR', 'Processing'),
        ('S',  'Shipped'),
        ('D',  'Delivered'),
    ]
    PAYMENT_CHOICES = [
        ('card', 'Paystack'),
        ('cod',  'Cash on Delivery'),
    ]

    payment_method  = models.CharField(max_length=4, choices=PAYMENT_CHOICES, default='card')
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        null=True, blank=True,
                                        on_delete=models.SET_NULL)
    created_at      = models.DateTimeField(auto_now_add=True)
    status          = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    total           = models.DecimalField(max_digits=10, decimal_places=2)
    reference       = models.CharField(max_length=100, blank=True, null=True)
    paid            = models.BooleanField(default=False)
    billing_name    = models.CharField(max_length=100, null=True)
    billing_email   = models.EmailField(null=True)
    billing_phone   = models.CharField(max_length=20, null=True)

    # ← Add these new fields ↓
    address_line1   = models.CharField(max_length=255, null=True, blank=True)
    address_line2   = models.CharField(max_length=255, null=True, blank=True)
    city            = models.CharField(max_length=100, null=True, blank=True)
    postcode        = models.CharField(max_length=20, null=True, blank=True)
    notes           = models.TextField(blank=True)

    def __str__(self):
        return f"Order {self.pk} – {self.get_status_display()}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
