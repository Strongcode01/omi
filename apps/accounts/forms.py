# app/accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    fullname = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username','email','phone','password1','password2', 'fullname')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email ')