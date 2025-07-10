# apps/orders/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from .models import Order, OrderItem
from .forms import CheckoutForm
from apps.cart.views import _get_cart
from apps.products.models import Product
import requests
from django.contrib.auth.decorators import login_required
from apps.payments.models import Payment as PaymentRecord
from django.contrib import messages
# Create your views here.

# apps/orders/views.py

def order_create(request):
    raw_cart = _get_cart(request)
    if not raw_cart:
        return redirect('products:product_list')

    # Build items & total
    items, total = [], 0
    for pid, qty in raw_cart.items():
        prod = get_object_or_404(Product, pk=pid)
        items.append({'product': prod, 'quantity': qty, 'subtotal': prod.price * qty})
        total += prod.price * qty

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # 1) Create the order
            order = Order.objects.create(
                user=request.user,
                total=total,
                billing_name=cd['full_name'],
                billing_email=cd['email'],
                billing_phone=cd['phone'],
                address_line1=cd['street_address'],
                address_line2=cd.get('address_line2', ''),
                city=cd['city'],
                postcode=cd['postcode'],
                notes=cd.get('notes', ''),
                payment_method=cd['payment_method'],   # ensure your Order model has this field
                status='P'  # Pending
            )

            # 2) Create order items
            for i in items:
                OrderItem.objects.create(
                    order=order,
                    product=i['product'],
                    quantity=i['quantity'],
                    price=i['product'].price
                )

            # 3) Clear the cart
            request.session['cart'] = {}

            # 4) Branch on payment method
            if cd['payment_method'] == 'cod':
                messages.success(request, "Order placed! You’ll pay on delivery.")
                return redirect('orders:order_detail', pk=order.pk)
            else:
                # Paystack path
                pay = PaymentRecord.objects.create(
                    order=order,
                    amount=int(total * 100),  # in kobo
                    email=cd['email']
                )
                return redirect('payments:make_payment', ref=pay.ref)
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {
        'form':       form,
        'items':      items,
        'cart_total': total,
    })


def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('items__product', 'payment'), pk=pk)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'payment': getattr(order, 'payment', None),
    })
