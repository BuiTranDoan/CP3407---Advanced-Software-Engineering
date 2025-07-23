from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', order_home, name='order_home'),
    path('order/', order, name='order'),
    path('order/detail/<int:pk>', order_detail, name='order_detail'),
    path('order/add', order_add, name='order_add'),
    path('order/<int:pk>', order_edit, name='order_edit'),
    path('order/delete/<int:pk>', order_delete, name='order_delete'),
    path('orderitem', orderitem, name='orderitem'),
    path('orderitem/add/<int:pk>/', orderitem_add, name='orderitem_add'),
    path('orderitem/edit/<int:pk>', orderitem_edit, name='orderitem_edit'),
    path('orderitem/<int:pk>', orderitem_detail, name='orderitem_detail'),
    path('orderitem/delete/<int:pk>', orderitem_delete, name='orderitem_delete'),
    path('orderitem/<int:pk>/customize/', orderitem_customization, name='orderitem_customization'),
]
