# apps/pages/forms.py
from django import forms
from .models import NewsletterSubscriber

class ContactForm(forms.Form):
    name     = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Name',
            'required': True,
        }))
    email    = forms.EmailField(widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email',
            'required': True,
        }))
    phone    = forms.CharField(max_length=20, required=False)
    usertype = forms.ChoiceField(choices=[
        ('regular','Regular User'),
        ('visitor','Visitor'),
        ('aquatic','Aquatic Stakeholder'),
        ('poultry','Poultry Stakeholder'),
    ], widget=forms.Select(attrs={'required':True
        }))
    message  = forms.CharField(widget=forms.Textarea(attrs={
            'placeholder': 'Your Message',
            'required': True,
            'rows': 4,
        }))

class SendMessageForm(forms.Form): # home page contact form
    name    = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Name',
            'required': True,
        })
    )
    email   = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email',
            'required': True,
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Your Message',
            'required': True,
            'rows': 4,
        })
    )

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
    def clean_email(self):
        email = self.cleaned_data['email']
        if NewsletterSubscriber.objects.filter(email=email).exists():
            raise forms.ValidationError("You're already subscribed.")
        return email

