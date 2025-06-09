from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = [
            'category',
            'subcategory',
            'species',
            'title',
            'description',
            'size',
            'price',
            'pond_type',
            'health_status',
            'treatment_recommendation',
            'image',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'treatment_recommendation': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # make the hierarchy fields optional with an empty label
        for fld in ('category', 'subcategory', 'species'):
            self.fields[fld].required    = False
            self.fields[fld].empty_label = '— None —'
        # treatment recommendation is always optional
        self.fields['treatment_recommendation'].required = False
