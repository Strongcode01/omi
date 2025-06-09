# app/accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignUpForm, LoginForm

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('products:product_list')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('products:product_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {
        'form': form
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:product_list')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Hello {user.username}, you are now logged in.')
            return redirect('products:product_list')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form
    })


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('products:product_list')
