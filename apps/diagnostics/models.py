from django.db import models
from django.conf import settings


# Create your models here.

class DiagnosticRequest(models.Model):
    STATUS = [('P','Pending'),('C','Completed')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sample_info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    result = models.TextField(blank=True)