from django.db import models

# Create your models here.
import secrets
from django.conf import settings

class Payment(models.Model):
    order       = models.OneToOneField(
        'orders.Order', related_name='payment', on_delete=models.CASCADE
    )
    ref         = models.CharField(
        max_length=100, unique=True, default=secrets.token_urlsafe
    )
    amount      = models.PositiveIntegerField()  # in kobo
    email       = models.EmailField()
    verified    = models.BooleanField(default=False)
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.ref} for Order {self.order.pk}"