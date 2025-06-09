from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.db import models


# Create your views here.

def product_list(request):
    # products = Product.objects.select_related('species__subcategory__category').all()
    q = request.GET.get('q', '').strip()
    base_qs = Product.objects.select_related('species__subcategory__category')
    if q:
        products = base_qs.filter(
            models.Q(title__icontains=q) |
            models.Q(description__icontains=q)
        )
    else:
        products = base_qs.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'q': q,
    })
    # return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def product_create(request):
    if not request.user.is_staff: return redirect('products:product_list')
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('products:product_list')
    return render(request, 'products/product_form.html', {'form': form})