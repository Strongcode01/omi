from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        label="Full Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Ebubechi Chinaza'
        })
    )

    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
        })
    )

    phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+234 800 000 0000'
        })
    )

    address_line1 = forms.CharField(
        label="Address Line 1",
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Street address, P.O. box'
        })
    )

    address_line2 = forms.CharField(
        label="Address Line 2",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apartment, suite, unit, etc. (optional)'
        })
    )
    house_no = forms.CharField(
        label = "House no",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'House and flat/room no (optional)'
        })
    )

    city = forms.CharField(
        label="City",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Lagos'
        })
    )

    postcode = forms.CharField(
        label="Postal Code",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 100001'
        })
    )

    PAYMENT_CHOICES = [
        ('card', 'Credit / Debit Card'),
        ('paypal', 'PayPal'),
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
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any special instructions?'
        })
    )
