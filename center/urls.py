from django.urls import path
from center.views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    ]