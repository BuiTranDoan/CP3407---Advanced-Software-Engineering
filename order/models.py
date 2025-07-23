from django.utils import timezone
from django.db import models
from menu.models import MenuItem, Customization

class Table(models.Model):
    TABLE_STATUS_CHOICES = [
        ('A', 'Available'),
        ('O', 'Occupied'), ]

    table_number = models.CharField(max_length=10, unique=True)
    seat = models.PositiveSmallIntegerField(default=2)
    table_status = models.CharField(max_length=1, choices=TABLE_STATUS_CHOICES, default='A')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Table {self.table_number}'

class Order(models.Model):
    STATUS_CHOICES = [
        ('R', 'Received'),
        ('P', 'Preparing'),
        ('C', 'Completed'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('P', 'Paid'),
        ('U', 'Unpaid'),
    ]

    order_number = models.CharField(max_length=10, unique=True, editable=False)
    table_number = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True, blank=True)
    # staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='R')
    notes = models.TextField(blank=True, null=True)
    payment = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default='U')

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()

        super().save(*args, **kwargs)

    def generate_order_number(self):
        today = timezone.now().date()
        today_orders = Order.objects.filter(created_at__date=today)

        if not today_orders.exists():
            new_number = 1
        else:
            # Extract the last 3 digits from the last order today
            last_order = today_orders.order_by('created_at').last()
            try:
                last_number = int(last_order.order_number.split('-')[-1])
            except:
                last_number = 0
            new_number = last_number + 1

        date_str = today.strftime('%Y%m%d')
        return f'{date_str}-{new_number:03}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def __str__(self):
        return f'#{self.order_number}, ({self.get_status_display()})'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    customizations = models.ManyToManyField(Customization, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    line_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_price(self):
        base_price = self.menu_item.price
        if self.pk: #really important cuz as a new instance will pass this instead of going through not existing(uncreated custom)
            for customization in self.customizations.all():
                base_price +=  customization.price
        return base_price

    def get_total_price(self):
        return self.get_price() * self.quantity

    def save(self, *args, **kwargs):
        self.unit_price = self.get_price()
        self.line_total = self.get_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity})"
