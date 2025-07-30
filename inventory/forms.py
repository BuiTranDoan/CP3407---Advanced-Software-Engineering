from django import forms
from inventory.models import Ingredient, IngredientPurchase, IngredientUsage, StockAudit


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit', 'description']

class StockAuditForm(forms.ModelForm):
    class Meta:
        model = StockAudit
        fields = ['actual_stock', 'notes']

    widgets = {
        'notes': forms.Textarea(attrs={'rows': 3}),
    }

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
        fields = ['date_used', 'ingredient', 'quantity']
        widgets = {
            'date_used': forms.DateInput(attrs={'type': 'date'})
        }
