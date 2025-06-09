from django import forms
from .models import DiagnosticRequest

class DiagnosticRequestForm(forms.ModelForm):
    class Meta:
        model = DiagnosticRequest
        fields = ('sample_info',)