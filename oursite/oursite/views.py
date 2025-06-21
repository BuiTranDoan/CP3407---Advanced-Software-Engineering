from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def inventory_page(request):
    return render(request, 'inventory.html')

def menu_page(request):
    return render(request, 'menu.html')

def order_page(request):
    return render(request, 'order.html')
