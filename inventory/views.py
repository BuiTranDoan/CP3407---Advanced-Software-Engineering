from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from inventory.models import Ingredient, IngredientUsage, IngredientPurchase
from inventory.forms import IngredientForm, IngredientPurchaseForm, IngredientUsageForm, StockAuditForm
from datetime import date
from decorators import *

def inventory(request):
    return render(request, 'inventory/inventory.html')

def ingredient_purchase(request):
    sort = request.GET.get('sort', 'purchased_at')
    direction = request.GET.get('dir', 'desc')

    # Add 'ingredient__name' to allowed sort fields
    allowed_fields = ['purchased_at', 'quantity', 'cost', 'ingredient__name']
    if sort not in allowed_fields:
        sort = 'purchased_at'

    order_by = f"-{sort}" if direction == 'desc' else sort
    ingredients = IngredientPurchase.objects.select_related('ingredient').order_by(order_by)

    return render(request, 'inventory/ingredient_purchase.html', {
        'ingredients': ingredients,
        'current_sort': sort,
        'current_dir': direction,
    })

@admin_required
def ingredient_purchase_add(request):
    if request.method == 'POST':
        form = IngredientPurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredient_purchase')
    else:
        form = IngredientPurchaseForm()
    return render(request, 'inventory/ingredient_purchase_form.html', {'form': form, 'title': 'Add Ingredient Purchase'})

@admin_required
def ingredient_purchase_edit(request, purchase_id):
    purchase = get_object_or_404(IngredientPurchase, id=purchase_id)
    if request.method == 'POST':
        form = IngredientPurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            return redirect('ingredient_purchase')
    else:
        form = IngredientPurchaseForm(instance=purchase)
    return render(request, 'inventory/ingredient_purchase_edit.html', {'form': form, 'purchase': purchase})

@admin_required
def ingredient_purchase_delete(request, purchase_id):
    purchase = get_object_or_404(IngredientPurchase, id=purchase_id)

    if request.method == 'POST':
        purchase.delete()
        return redirect('ingredient_purchase')

    return render(request, 'inventory/ingredient_purchase_delete.html', {'purchase': purchase})

def ingredient_usage(request):
    sort = request.GET.get('sort', 'date_used')
    direction = request.GET.get('dir', 'desc')

    allowed_fields = ['date_used', 'ingredient__name', 'quantity', 'menu_item']
    if sort not in allowed_fields:
        sort = 'date_used'

    order_by = f"-{sort}" if direction == 'desc' else sort
    ingredient_usage_all = IngredientUsage.objects.select_related('ingredient').order_by(order_by)

    return render(request, 'inventory/ingredient_usage.html', {
        'ingredient_usage_all': ingredient_usage_all,
        'current_sort': sort,
        'current_dir': direction,
    })

@admin_required
def ingredient_usage_add(request):
    if request.method == 'POST':
        form = IngredientUsageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredient_usage')
    else:
        form = IngredientUsageForm(initial={'date_used': date.today()})
    return render(request, 'inventory/ingredient_usage_add.html', {'form': form})

@admin_required
def ingredient_usage_edit(request, usage_id):
    usage = get_object_or_404(IngredientUsage, id=usage_id)
    if request.method == 'POST':
        form = IngredientUsageForm(request.POST, instance=usage)
        if form.is_valid():
            form.save()
            return redirect('ingredient_usage')
    else:
        form = IngredientUsageForm(instance=usage)
    return render(request, 'inventory/ingredient_usage_edit.html', {'form': form})

@admin_required
def ingredient_usage_delete(request, usage_id):
    usage = get_object_or_404(IngredientUsage, id=usage_id)
    if request.method == 'POST':
        usage.delete()
        return redirect('ingredient_usage')
    return render(request, 'inventory/ingredient_usage_delete.html', {'usage': usage})


def ingredients(request):
    ingredients_list = Ingredient.objects.all()
    return render(request, 'inventory/ingredients.html', {'ingredients': ingredients_list})

@admin_required
def ingredient_add(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredients')
    else:
        form = IngredientForm()
    return render(request, 'inventory/ingredient_add.html', {'form': form, 'title': 'Add Ingredient'})

@admin_required
def ingredient_edit(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('ingredients')
    else:
        form = IngredientForm(instance=ingredient)
    return render(request, 'inventory/ingredient_edit.html', {'form': form, 'ingredient': ingredient, 'title': 'Edit Ingredient'})


def ingredient_detail(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    return render(request, 'inventory/ingredient_detail.html', {'ingredient': ingredient})

@admin_required
def ingredient_delete(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('ingredients')
    return render(request, 'inventory/ingredient_delete.html', {'ingredient': ingredient})

@admin_required
def stock_audit_add(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    if request.method == 'POST':
        form = StockAuditForm(request.POST)
        if form.is_valid():
            stock_audit = form.save(commit=False)
            stock_audit.ingredient = ingredient
            stock_audit.save()
            return redirect('ingredient_detail', ingredient_id=ingredient.id)
    else:
        form = StockAuditForm()
    return render(request, 'inventory/stock_audit_form.html', {'form': form, 'ingredient': ingredient})