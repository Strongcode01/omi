from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self): return self.name or '—'

class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='subcategories',
        blank=True,
        null=True
    )
    name = models.CharField(max_length=100)
    def __str__(self): 
        if self.category:
            return f"{self.category.name} > {self.name}"
        return self.name

class Species(models.Model):
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        related_name='species',
        blank=True,
        null=True
    )
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Product(models.Model):
    POND_TYPE_CHOICES = [
        ('earthen', 'Earthen Pond'),
        ('concrete', 'Concrete Pond'),
        ('cage', 'Cage Pond'),
        ('tarpaulin', 'Tarpaulin Pond'),
        ('plastic', 'Plastic Pond'),
    ]
    HEALTH_STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('treated', 'Previously Treated'),
        ('never_sick', 'Never Sick'),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True
    )
    species = models.ForeignKey(
        Species,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True
    )
    title                   = models.CharField(max_length=255)
    description             = models.TextField()
    size                    = models.CharField(max_length=50)
    price                   = models.DecimalField(max_digits=10, decimal_places=2)
    pond_type               = models.CharField(max_length=50, choices=POND_TYPE_CHOICES)
    health_status           = models.CharField(max_length=20, choices=HEALTH_STATUS_CHOICES)
    treatment_recommendation = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Optional: recommended vaccine/treatment"
    )
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
