from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Count, F
from datetime import datetime
from order.models import Order, OrderItem, Table
from inventory.models import Ingredient
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Get date from GET parameter or default to today
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = datetime.today().date()
    else:
        selected_date = datetime.today().date()

    # --- Sales Summary ---
    orders = Order.objects.filter(created_at__date=selected_date)
    total_sales = sum(order.get_total_price() for order in orders)
    total_orders = orders.count()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0

    # --- Top-Selling Items ---
    top_items = (
        OrderItem.objects.filter(order__created_at__date=selected_date)
        .values('menu_item__name')
        .annotate(quantity_sold=Sum('quantity'), total_revenue=Sum('line_total'))
        .order_by('-quantity_sold')[:5]
    )

    # --- Table Usage ---
    tables = Table.objects.filter(is_active=True)
    table_data = []
    for table in tables:
        table_orders = orders.filter(table_number=table)
        table_data.append({
            'table_number': table.table_number,
            'status': table.get_table_status_display(),
            'order_count': table_orders.count(),
            'total_sales': sum(order.get_total_price() for order in table_orders),
        })

    # --- Low Stock Ingredients ---
    low_stock_ingredients = []
    for ingredient in Ingredient.objects.all():
        threshold = ingredient.last_actual_stock()
        if threshold is not None and ingredient.stock_level() < threshold:
            low_stock_ingredients.append({
                'name': ingredient.name,
                'stock': ingredient.stock_level(),
                'unit': ingredient.unit,
                'threshold': threshold
            })

    context = {
        'selected_date': selected_date,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'top_items': top_items,
        'table_data': table_data,
        'low_stock_ingredients': low_stock_ingredients,
    }

    return render(request, 'center/dashboard.html', context)
