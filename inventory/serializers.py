from rest_framework import serializers
from .models import Category, InventoryItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class InventoryItemSerializer(serializers.ModelSerializer):

    category = CategorySerializer(serializers.ModelSerializer)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category',
    )

    class Meta:
        model = InventoryItem
        fields = [
            'id',
            'name',
            'category',
            'category_id',
            'unit',
            'quantity',
            'threshold',
            'supplier',
            'last_updated',
        ]
        read_only_fields = ['last_updated']
