from django.db import models
from django.utils import timezone

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    stock_level = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name

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
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE)    # How much of the ingredient is used in that menu item
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} of {self.ingredient.name} for {self.menu_item.name}"

    def save(self, *args, **kwargs):
        # Adjusts the stock level on save (subtracts used quantity)
        if self.pk:  # Editing existing record
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

