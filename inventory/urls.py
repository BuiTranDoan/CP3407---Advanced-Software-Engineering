from django.urls import path, include
from inventory.views import *

urlpatterns = [
    path('', inventory, name='inventory'),
    path('ingredient/purchase/', ingredient_purchase, name='ingredient_purchase'),
    path('ingredient/purchase/add', ingredient_purchase_add, name='ingredient_purchase_add'),
    path('ingredient/purchase/<int:purchase_id>', ingredient_purchase_edit, name='ingredient_purchase_edit'),
    path('ingredient/purchase/<int:purchase_id>/delete/', ingredient_purchase_delete, name='ingredient_purchase_delete'),

    path('ingredient/usage/', ingredient_usage, name='ingredient_usage'),
    path('ingredient/usage/add/', ingredient_usage_add, name='ingredient_usage_add'),
    path('ingredient/usage/edit/<int:usage_id>/', ingredient_usage_edit, name='ingredient_usage_edit'),
    path('ingredient/usage/delete/<int:usage_id>/', ingredient_usage_delete, name='ingredient_usage_delete'),

    path('ingredients/', ingredients, name='ingredients'),
    path('ingredients/add/', ingredient_add, name='ingredient_add'),
    path('ingredient/<int:ingredient_id>/', ingredient_detail, name='ingredient_detail'),
    path('ingredient/edit/<int:ingredient_id>/', ingredient_edit, name='ingredient_edit'),
    path('ingredient/delete/<int:ingredient_id>/', ingredient_delete, name='ingredient_delete'),

    path('ingredienta/<int:ingredient_id>/add_audit/', stock_audit_add, name='stock_audit_add'),


]