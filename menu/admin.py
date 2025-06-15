from django.contrib import admin
from .models import Category, Customization, MenuItem

# admin.site.register((Category, Customization, MenuItem))

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')        # Adds columns in list view
    search_fields = ('name',)                     # Adds search bar for 'name' field

@admin.register(Customization)
class CustomizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    search_fields = ('name',)
    list_filter = ('category', 'is_available')    # Adds filter sidebar

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    search_fields = ('name', 'description')
    list_filter = ('category', 'is_available')