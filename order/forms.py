from django import forms
from .models import *

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'status', 'payment', 'notes']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']

class CustomizationsForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['customizations']
        widgets = {
            'customizations': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.menu_item:
            self.fields['customizations'].queryset = Customization.objects.filter(
                category=self.instance.menu_item.category,
                is_available=True
            )