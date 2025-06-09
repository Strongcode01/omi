from django.shortcuts import redirect, render, get_object_or_404
from apps.products.models import Product
# Create your views here.

SESSION_CART_KEY = 'cart'


def _get_cart(request):
    return request.session.get(SESSION_CART_KEY, {})


def cart_detail(request):
    cart = _get_cart(request)
    items = []
    total = 0
    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=pid)
        subtotal = product.price * qty
        total += subtotal
        items.append({'product':product,'quantity':qty,'subtotal':subtotal})
    return render(request, 'cart/cart_detail.html', {'items': items, 'total': total})


def cart_add(request, pk):
    cart = _get_cart(request)
    cart[str(pk)] = cart.get(str(pk),0) + 1
    request.session[SESSION_CART_KEY] = cart
    return redirect('cart:cart_detail')

def cart_deduct(request, pk):
    """
    Subtracts 1 from the quantity of product `pk` in the session cart.
    If the resulting quantity is <= 0, removes the product entirely.
    """
    cart = _get_cart(request)
    key = str(pk)

    # Current quantity (0 if not present)
    current_qty = cart.get(key, 0)

    if current_qty > 1:
        # Simply decrement
        cart[key] = current_qty - 1
    elif current_qty == 1:
        # If it would go to zero, remove the item
        cart.pop(key, None)
    else:
        # Item wasn't in cart to begin with; you could log or message here if you like
        pass

    # Save back to session
    request.session[SESSION_CART_KEY] = cart

    return redirect('cart:cart_detail')



def cart_update(request, pk):
    """
    Sets the quantity of product `pk` in the cart to the posted value.
    If qty ≤ 0, removes the item.
    """
    cart = _get_cart(request)
    if request.method == 'POST':
        try:
            qty = int(request.POST.get('quantity', 1))
        except ValueError:
            qty = 1

        if qty > 0:
            cart[str(pk)] = qty
        else:
            cart.pop(str(pk), None)

        request.session[SESSION_CART_KEY] = cart

    return redirect('cart:cart_detail')


def cart_remove(request, pk):
    cart = _get_cart(request)
    if str(pk) in cart:
        del cart[str(pk)]
        request.session[SESSION_CART_KEY] = cart
    return redirect('cart:cart_detail')