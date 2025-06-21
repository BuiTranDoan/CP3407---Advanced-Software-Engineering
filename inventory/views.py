from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import F

from .models import Category, InventoryItem
from .serializers import CategorySerializer, InventoryItemSerializer

from rest_framework import filters

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'supplier']

    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        low_stock_items = self.queryset.filter(quantity__lt=F('threshold'))
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)