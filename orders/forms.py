# orders/forms.py

from django import forms
from .models import Order

class OrderCreationForm(forms.ModelForm):
    # This form is intentionally minimal as most data (client, seller, service, price) 
    # is set automatically in the view upon clicking "Order Now".
    class Meta:
        model = Order
        fields = [] # No user-editable fields needed for the initial click

# Form for the seller to update the status of an order
class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }