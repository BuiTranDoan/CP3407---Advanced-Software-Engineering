from wsgiref.util import request_uri

from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Category, Customization, MenuItem
from .serializers import CategorySerializer, CustomizationSerializer, MenuItemSerializer
from .forms import *

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomizationViewSet(viewsets.ModelViewSet):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminUser]

def menu(request):
    return render(request, 'menu/menu_home.html')

def category(request):
    categories = Category.objects.all()
    return render(request, 'menu/category.html', {'categories': categories})

def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        form = CategoryForm()
    return render(request, 'menu/category_add_edit.html', {'form': form})

def category_edit(request, pk):
    category_obj = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category_obj)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        form = CategoryForm(instance=category_obj)
    return render(request, 'menu/category_add_edit.html', {'form':form})

def category_delete(request, pk):
    category_obj = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        category_obj.delete()
        return redirect('category')
    return render(request, 'menu/category_delete_confirm.html', {'category_obj':category_obj})


def customization(request):
    customizations = Customization.objects.all()
    return render(request, 'menu/customization.html', {'customizations': customizations})

def customization_add(request):
    if request.method == 'POST':
        form = CustomizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customization')
    else:
        form = CustomizationForm()
    return render(request, 'menu/customization_add_edit.html', {'form': form})

def customization_edit(request, pk):
    customization_obj = get_object_or_404(Customization, id=pk)
    if request.method == 'POST':
        form = CustomizationForm(request.POST, instance=customization_obj)
        if form.is_valid():
            form.save()
            return redirect('customization')
    else:
        form = CustomizationForm(instance=customization_obj)
    return render(request, 'menu/customization_add_edit.html', {'form':form})

def customization_delete(request, pk):
    customization_obj = get_object_or_404(Customization, id=pk)
    if request.method == 'POST':
        customization_obj.delete()
        return redirect('customization')
    return render(request, 'menu/customization_delete_confirm.html', {'customization_obj':customization_obj})


def menu_list_view(request):
    items = MenuItem.objects.all()
    return render(request, 'menu/menu_list.html', {'items': items})

def menu_add(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm()
        return render(request, 'menu/menu_add_edit.html', {'form': form})

def menu_edit(request, pk):
    item = get_object_or_404(MenuItem, id=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'menu/menu_edit.html', {'form': form, 'item': item})

def menu_delete(request, pk):
    item = get_object_or_404(MenuItem, id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('menu_list')
    return render(request, 'menu/menu_delete_confirm.html', {'item':item})
