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

def menu(request):
    return render(request, 'menu/menu_home.html')

def menu_list_view(request):
    items = MenuItem.objects.all()
    return render(request, 'menu/menu_list.html', {'items': items})

def customization(request):
    return render(request, 'menu/customization.html')

