from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'customizations', CustomizationViewSet)
router.register(r'menu-items', MenuItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', menu, name='menu'),
    path('category/', category, name='category'),
    path('category/add/', category_add, name='category_add'),
    path('category/<int:pk>/', category_edit, name='category_edit'),
    path('category/delete/<int:pk>/', category_delete, name='category_delete'),
    path('customization/', customization, name='customization'),
    path('customization/add/', customization_add, name='customization_add'),
    path('customization/<int:pk>/', customization_edit, name='customization_edit'),
    path('customization/delete/<int:pk>', customization_delete, name='customization_delete'),
    path('menu/', menu_list_view, name='menu_list'),
    path('menu/add/', menu_add, name='menu_add'),
    path('menu/<int:pk>/', menu_edit, name='menu_edit'),
    path('menu/delete/<int:pk>', menu_delete, name='menu_delete'),
]