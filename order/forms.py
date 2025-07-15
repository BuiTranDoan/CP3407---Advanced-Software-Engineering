from django import forms
from .models import *

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'status', 'payment', 'notes']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'customizations', 'quantity', 'unit_price']
        widgets = {
            'customizations': forms.CheckboxSelectMultiple,
        }