# context_processors.py
from .views import _get_cart
from apps.products.models import Product

def cart_items(request):
    cart = _get_cart(request)
    items, total = [], 0
    for pid, qty in cart.items():
        product = Product.objects.get(pk=pid)
        subtotal = product.price * qty
        items.append({
            'product': product,
            'quantity': qty,
            'subtotal': subtotal,
        })
        total += subtotal
    return {'items': items, 'total': total}
