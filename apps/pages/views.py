from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from apps.pages.forms import ContactForm, NewsletterForm, SendMessageForm
from apps.products.models import Product, Category, SubCategory, Species
from django.views.generic import TemplateView
from django.core.mail import EmailMessage

def home(request, sent=False, form=None):
    featured   = Product.objects.all().order_by('-created_at')[:4]
    categories = Category.objects.prefetch_related('subcategories').all()
    newsletter_form = NewsletterForm()
    # Static testimonials and FAQs (could be pulled from DB later)
    testimonials = [
        {'user': 'Strongcode Udo',    'role': 'Restaurant Owner',
         'text': 'OMI’s quality and speed are unmatched. Our stock never looked better!'},
        {'user': 'John Nwokoro',  'role': 'Broodstock Farmer',
         'text': 'The PCR diagnostics integration saved my stock from disease outbreak.'},
        {'user': 'Alice Iganga.',    'role': 'Home Consumer',
         'text': 'Easy ordering and prompt delivery–highly recommend OMI!'},
    ]
    faqs = [
        {'q': 'How do I place an order?', 
         'a': 'Browse products, add to cart, then checkout with your details.'},
        {'q': 'What payment methods are supported?',
         'a': 'We support Paystack for secure card payments and bank transfers.'},
        {'q': 'How do I request a PCR test?',
         'a': 'Go to Diagnostics → New Request, fill the form, and our team will follow up.'},
    ]
    if form is None:
        send_message_form, contact_form = SendMessageForm(), ContactForm
    else:
        send_message_form = form

    return render(request, 'home.html', {
        'products':    featured,
        'categories':  categories,
        'testimonials': testimonials,
        'faqs':         faqs,
        'send_message_form': send_message_form,
        'contact_form': contact_form,
        'sent': sent,
     })

def send_message(request):
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"OMI Message from {cd['name']}"
            body = (
                f"Name: {cd['name']}\n"
                f"Email: {cd['email']}\n\n"
                f"Message:\n{cd['message']}"
            )

            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.DEFAULT_FROM_EMAIL],
                headers={'Reply-To': cd['email']},
            )
            email.send(fail_silently=False)
            return home(request, sent=True)
        return home(request, sent=False, form=form)

    return redirect('pages:home')

# 1. The page view that displays the contact form
def contact_us(request, sent=False, form=None):
    """
    Renders the contact page. If `sent=True`, a success popup will appear.
    If `form` is provided (with validation errors), it is re-rendered.
    """
    # Always instantiate a NewsletterForm if you need it in your template:
    newsletter_form = NewsletterForm()

    # Decide which ContactForm to render
    if form is None:
        contact_form = ContactForm()
    else:
        contact_form = form

    return render(request, 'contact.html', {
        'contact_form':   contact_form,
        'newsletter_form': newsletter_form,
        'sent':           sent,
    })

# 2. The function that processes a POST from the contact form
def contact_submit(request):
    """
    Handles form submission from /contact/ (Contact page). On success,
    it re-calls contact_us(...) with sent=True so the popup shows.
    On validation failure, re-calls contact_us(...) with the bound form.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"Contact from {cd['name']}"

            body = (
                f"Name:  {cd['name']}\n"
                f"Email: {cd['email']}\n"
                f"Phone: {cd['phone']}\n"
                f"User Type: {cd['usertype']}\n\n"
                f"Message:\n{cd['message']}"
            )

            # Use EmailMessage so we can set a Reply-To header
            email_msg = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,    # e.g. "yourgmail@gmail.com"
                to=[settings.ADMIN_EMAIL],                 # ensure ADMIN_EMAIL is set in settings.py
                headers={'Reply-To': cd['email']},
            )
            email_msg.send(fail_silently=False)

            # Re-render contact_us view with sent=True so the popup appears
            return contact_us(request, sent=True)

        # If the form is invalid, re-render contact_us with the bound form (showing errors)
        return contact_us(request, sent=False, form=form)

    # If someone accesses /contact_submit/ via GET, redirect to the contact page
    return redirect('pages:contact_us')

def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            # Optionally send a welcome email:
            send_mail(
                subject="Thanks for subscribing!",
                message="Welcome to the OMI newsletter.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
            )
            return render(request, 'newsletter_success.html', {'email': subscriber.email})
    else:
        form = NewsletterForm()
    return redirect('pages:home') 


class ContactPageView(TemplateView):
    template_name = 'contact.html'


class ServicesPageView(TemplateView):
    template_name = 'services.html'    
