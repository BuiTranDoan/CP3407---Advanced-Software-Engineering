from django.contrib import admin
from .models import Category, InventoryItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'unit', 'threshold', 'last_updated')
    search_fields = ('name', 'supplier')
    list_filter = ('category', 'supplier')
    ordering = ('-last_updated',)

