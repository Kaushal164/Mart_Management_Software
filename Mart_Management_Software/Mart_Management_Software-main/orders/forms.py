from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_email', 'customer_address', 'payment_method', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                'required': True,
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+977-98XXXXXXXX',
                'required': True,
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com',
            }),
            'customer_address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Delivery address (e.g., Thamel, Kathmandu)',
                'rows': 3,
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any special instructions...',
                'rows': 2,
            }),
        }
