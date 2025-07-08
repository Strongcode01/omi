import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings

from apps.orders.paystack import Paystack
from .models import Order, OrderItem, Payment
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
    # 1. Fetch raw cart data and prepare items + total for summary
    raw_cart = _get_cart(request)  # e.g. {'1': 2, '5': 1}
    if not raw_cart:
        return redirect('products:product_list')

    items = []
    cart_total = 0
    for pid, qty in raw_cart.items():
        product = Product.objects.get(pk=pid)
        subtotal = product.price * qty
        items.append({
            'product':  product,
            'quantity': qty,
            'subtotal': subtotal,
        })
        cart_total += subtotal

    # 2. Handle form submission
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Create Order
            order = Order.objects.create(user=request.user, total=0)
            total = 0
            for pid, qty in raw_cart.items():
                product = Product.objects.get(pk=pid)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=product.price
                )
                total += product.price * qty
            order.total = total
            order.save()

            # Clear cart
            request.session['cart'] = {}

            # Create Payment record
            pay = Payment.objects.create(
                order=order,
                amount=int(total * 100),  # amount in kobo
                email=cd['email']
            )

            # Redirect to Paystack checkout page
            return redirect('orders:make_payment', ref=pay.ref)
    else:
        form = CheckoutForm()

    # 3. Render the checkout page — always include items + cart_total
    return render(request, 'orders/checkout.html', {
        'form':       form,
        'items':      items,
        'cart_total': cart_total,
    })
def make_payment(request, ref):
    """
    Show the “Make Payment” page with Paystack inline JS.
    """
    payment = get_object_or_404(Payment, ref=ref)
    order   = payment.order
    context = {
        'order': order,
        'payment': payment,
        'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'orders/make_payment.html', context)

def verify_payment(request, ref):
    """
    Called by Paystack callback. Verifies then shows thank-you.
    """
    payment = get_object_or_404(Payment, ref=ref)
    success, data = Paystack().verify_payment(ref)
    if success and data.get('amount') == payment.amount:
        payment.verified = True
        payment.save()
        # optionally update order.status
        order = payment.order
        order.status = 'PR'
        order.save()
        messages.success(request, "Payment successful!")
        return render(request, 'orders/thankyou.html', {
            'order': order,
            'payment': payment
        })
    messages.error(request, "Payment verification failed.")
    return redirect('orders:order_detail', pk=payment.order.pk)

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
    # Fetch order and its items
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product', 'payment'),
        pk=pk
    )
    # Grab the one‑to‑one Payment if it exists
    payment = getattr(order, 'payment', None)

    return render(request, 'orders/order_detail.html', {
        'order':   order,
        'payment': payment,
    })