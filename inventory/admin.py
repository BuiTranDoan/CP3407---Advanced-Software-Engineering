from django.contrib import admin
from inventory.models import IngredientUsage, Ingredient, IngredientPurchase, StockAudit


#admin.site.register(IngredientUsage)
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'description', 'stock_level')

admin.site.register(IngredientUsage)
admin.site.register(IngredientPurchase)
admin.site.register(StockAudit)