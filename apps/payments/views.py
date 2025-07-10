from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Payment
from .paystack import Paystack
from django.conf import settings


def make_payment(request, ref):
    payment = get_object_or_404(Payment, ref=ref)
    return render(request, 'payments/make_payment.html', {
        'payment': payment,
        'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
    })


def verify_payment(request, ref):
    payment = get_object_or_404(Payment, ref=ref)
    success, data = Paystack().verify_payment(ref)
    if success and data.get('amount') == payment.amount:
        payment.verified = True
        payment.save()
        return render(request, 'payments/thank_you.html', {'payment': payment})
    return redirect('orders:order_detail', pk=payment.order.pk)


@csrf_exempt
def webhook(request):
    # minimal Paystack webhook handler
    return HttpResponse(status=200)