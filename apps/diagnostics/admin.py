from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DiagnosticRequest

@admin.register(DiagnosticRequest)
class DiagnosticRequestAdmin(admin.ModelAdmin):
    list_display = ('id','user','status','created_at')
    list_filter = ('status','created_at')