import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Order, OrderItem
from .forms import CheckoutForm
from apps.cart.views import _get_cart
from apps.products.models import Product
import requests
from uuid import uuid4
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.

# @login_required(login_url='accounts:login')
def order_create(request):
    cart = _get_cart(request)
    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect('products:product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # 1. Create order and items
            order = Order.objects.create(
                user=request.user,
                total=0,
                reference='',
                paid=False
            )
            total = 0
            for pid, qty in cart.items():
                product = Product.objects.get(pk=pid)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=product.price
                )
                total += product.price * qty

            order.total = total
            order.reference = f"{order.pk}_{uuid4().hex}"
            order.save()
            # 2. Clear cart
            request.session['cart'] = {}

            # 3. Render payment page
            return render(request, 'orders/payment.html', {
                'order': order,
                'form': form,
                'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
            })
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {'form': form})


# Callback view
@csrf_exempt
def payment_callback(request):
    reference = request.GET.get('reference')
    if not reference:
        return redirect('products:product_list')
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
    resp = requests.get(url, headers=headers)
    data = resp.json()
    # Extract order pk
    order_pk = reference.split('_')[0]
    order = Order.objects.get(pk=order_pk)
    if data.get('status') and data['data']['status']== 'success':
        order.paid = True
        order.status = 'PR'  # Processing
        order.save()
        return redirect('orders:order_detail', pk=order.pk)
    else:
        messages.error(request, "Payment verification failed.")
        return redirect('orders:order_detail', pk=order.pk)
    
@csrf_exempt
def paystack_webhook(request):
    payload = request.body
    signature = request.headers.get('x-paystack-signature')

    try:
        data = json.loads(payload)
        if data.get('event') == 'charge.success':
            reference = data['data']['reference']
            order_id = reference.split('_')[0]
            try:
                order = Order.objects.get(id=order_id, reference=reference)
                if order.status == 'P':
                    order.status = 'PR'  # Update to "Processing"
                    order.save()
                    return HttpResponse(status=200)
            except Order.DoesNotExist:
                return HttpResponse("Order not found", status=404)
    except json.JSONDecodeError:
        return HttpResponse("Invalid payload", status=400)

    return HttpResponse("Unhandled", status=200)


def order_detail(request, pk):
    order = Order.objects.prefetch_related('items__product').get(pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})