from django.contrib import admin
from .models import Category, SubCategory, Species, Product

# Register your models here.


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Species)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','species','price','pond_type','size','health_status','created_at')
    list_filter = ('species__subcategory__category','pond_type','size')