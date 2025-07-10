from django import forms
from .models import Category, Customization, MenuItem
from django.utils.safestring import mark_safe
from django.urls import reverse

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class CustomizationForm(forms.ModelForm):
    class Meta:
        model = Customization
        fields = ['name', 'category', 'description', 'price', 'is_available']