from django import forms
from inventory.models import Ingredient, IngredientPurchase, IngredientUsage

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'stock_level', 'unit']

class IngredientPurchaseForm(forms.ModelForm):
    class Meta:
        model = IngredientPurchase
        fields = ['ingredient', 'quantity', 'cost', 'purchased_at']
        widgets = {
            'purchased_at': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'ingredient': 'Select Ingredient',
            'quantity': 'Quantity Purchased',
            'cost': 'Total Cost (S$)',
            'purchased_at': 'Purchase Date',
        }

class IngredientUsageForm(forms.ModelForm):
    class Meta:
        model = IngredientUsage
        fields = ['ingredient', 'menu_item', 'quantity']
