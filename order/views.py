from rest_framework import viewsets
from .models import Order, OrderItem
from .forms import OrderForm
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404, render, redirect

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

def order_home(request):
    return render(request, 'order_home.html')

def order(request):
    orders = Order.objects.all()
    return render(request, 'order.html', {'orders':orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, id=pk)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})

def order_add(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()

            return redirect('order_detail', pk=order.id)
    else:
        form = OrderForm()
    return render(request, 'order_add.html', {'form': form})

def order_edit(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_detail', pk=pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'order_edit.html', {'form': form, 'order': order})

def order_delete(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order')
    return render(request, 'order_delete.html', {'order': order})

def orderitem(request):
    orderitems = OrderItem.objects.all()
    for orderitem in orderitems:
        orderitem.save()
        orderitem.refresh_from_db()
    return render(request, 'orderitem.html', {'orderitems':orderitems})

def orderitem_add(request):
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()

            return redirect('order_detail', pk=order.id)
    else:
        form = OrderForm()
    return render(request, 'order_add.html', {'form': form})

def orderitem_detail(request, pk):
    orderitem = get_object_or_404(OrderItem, id=pk)
    return render(request, 'orderitem_detail.html', {'orderitem': orderitem})

def orderitem_edit(request, pk):
    pass

def orderitem_delete(request, pk):
    pass
