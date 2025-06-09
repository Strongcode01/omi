from django.shortcuts import render, redirect
from django.conf import settings
from .models import Order, OrderItem
from .forms import CheckoutForm
from apps.cart.views import _get_cart
from apps.products.models import Product

# Create your views here.



def order_create(request):
    cart = _get_cart(request)
    if not cart: return redirect('products:product_list')
    if request.method=='POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            total = 0
            order = Order.objects.create(
                user=request.user,
                total=0
            )
            for pid, qty in cart.items():
                product = Product.objects.get(pk=pid)
                price = product.price
                OrderItem.objects.create(
                    order=order, product=product, quantity=qty, price=price
                )
                total += price*qty
            order.total = total
            order.save()
            request.session['cart'] = {}
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = CheckoutForm()
    return render(request, 'orders/checkout.html', {'form': form})


def order_detail(request, pk):
    order = Order.objects.prefetch_related('items__product').get(pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})