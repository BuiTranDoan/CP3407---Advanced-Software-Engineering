from django.urls import path, include
from inventory.views import *

urlpatterns = [
    path('', inventory, name='inventory'),
    path('ingredients/', ingredients, name='ingredients'),
    path('ingredients/add/', ingredient_add, name='ingredient_add'),
    path('ingredient/<int:ingredient_id>', ingredient_detail, name='ingredient_detail'),
    path('ingredient/<int:ingredient_id>/delete/', ingredient_delete, name='ingredient_delete'),
    path('ingredient/', ingredient_usage, name='ingredient_usage'),
    path('ingredient/usage/', ingredient_usage_add, name='ingredient_usage_add'),
    path('ingredient/purchase/', ingredient_purchase, name='ingredient_purchase'),
    path('ingredient/purchase/add', ingredient_purchase_add, name='ingredient_purchase_add'),
    path('ingredient/purchase/<int:purchase_id>', ingredient_purchase_edit, name='ingredient_purchase_edit'),
path('ingredient/purchase/<int:purchase_id>/delete/', ingredient_purchase_delete, name='ingredient_purchase_delete'),
]