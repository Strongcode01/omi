# app/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)