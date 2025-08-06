from django.urls import path
from .views import *
urlpatterns = [
    path('', staff_home, name='staff_home'),
    path('staff/', staff_list, name='staff'),
    path('add/', staff_add, name='staff_add'),
    path('edit/<int:user_id>/', staff_edit, name='staff_edit'),
    path('delete/<int:user_id>/', staff_delete, name='staff_delete'),

    path('shift/', shift, name='shift'),
    path('shift/add/', shift_add, name='shift_add'),
    path('shift/edit/<int:shift_id>/', shift_edit, name='shift_edit'),
    path('shift/delete/<int:shift_id>/', shift_delete, name='shift_delete'),

path('worklogs/', worklog_list, name='worklog_list'),
    path('clock-in/<int:staff_id>/<int:shift_id>/', clock_in, name='clock_in'),
    path('clock-out/<int:staff_id>/<int:shift_id>/', clock_out, name='clock_out'),
]