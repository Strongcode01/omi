from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        label="Full Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    street_address = forms.CharField(
        label="Street Address",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    address_line2 = forms.CharField(
        label="Address Line 2",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    city = forms.CharField(
        label="City",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    postcode = forms.CharField(
        label="Postal Code",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    PAYMENT_CHOICES = [
        ('card', 'Paystack (Card/Bank Transfer)'),
        ('cod', 'Cash on Delivery'),
    ]
    payment_method = forms.ChoiceField(
        label="Payment Method",
        choices=PAYMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    notes = forms.CharField(
        label="Order Notes",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )