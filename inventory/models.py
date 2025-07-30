from datetime import datetime
from django.db import models
from django.utils import timezone

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    # stock_level = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def stock_level(self):
        return self.total_purchase() - self.total_use()

    def total_purchase(self):
        return self.ingredientpurchase_set.aggregate(total=models.Sum('quantity'))['total'] or 0

    def total_use(self):
        return self.ingredientusage_set.aggregate(total=models.Sum('quantity'))['total'] or 0

    def remaining_stock(self):
        return self.stock_level

    def last_audit(self):
        return self.stockaudit_set.order_by('-recorded_at').first()

    def last_actual_stock(self):
        last_audit = self.stockaudit_set.order_by('-recorded_at').first()
        return last_audit.actual_stock if last_audit else None

    def latest_cost_per_unit(self):
        latest_purchase = self.ingredientpurchase_set.order_by('-purchased_at').first()
        if latest_purchase:
            return round(latest_purchase.cost / latest_purchase.quantity, 2)
        return None


class IngredientPurchase(models.Model):
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} of {self.ingredient.name} at S${self.cost}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.ingredient.stock_level += self.quantity
            self.ingredient.save()
        super().save(*args, **kwargs)

class IngredientUsage(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)    # Links to the menu item where the ingredient is used
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE, null=True, blank=True)    # How much of the ingredient is used in that menu item
    date_used = models.DateField(default=datetime.now)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} of {self.ingredient.name} on {self.date_used}"

    def save(self, *args, **kwargs):
        # Adjusts the stock level on save (subtracts used quantity)
        if self.pk:
            original = IngredientUsage.objects.get(pk=self.pk)
            quantity_difference = self.quantity - original.quantity
        else:  # New usage
            quantity_difference = self.quantity

        self.ingredient.stock_level -= quantity_difference
        self.ingredient.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Reverts stock when a usage record is deleted
        self.ingredient.stock_level += self.quantity
        self.ingredient.save()
        super().delete(*args, **kwargs)

class StockAudit(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    actual_stock = models.PositiveIntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def expected_stock(self):
        return self.ingredient.stock_level

    def discrepancy(self):
        return self.actual_stock - self.expected_stock()

    def __str__(self):
        return f"Audit for {self.ingredient.name} at {self.recorded_at.strftime('%Y-%m-%d')}"