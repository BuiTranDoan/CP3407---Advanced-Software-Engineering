from django.urls import path
from .views import staff_list, staff_add, staff_edit, staff_delete
urlpatterns = [
    path('', staff_list, name='staff_list'),
    path('add/', staff_add, name='staff_add'),
    path('edit/<int:user_id>/', staff_edit, name='staff_edit'),
    path('delete/<int:user_id>/', staff_delete, name='staff_delete'),
]