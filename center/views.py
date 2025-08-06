from django.shortcuts import render
from datetime import datetime, date, timedelta
from django.db.models import Sum, Count
from collections import defaultdict
from order.models import Order, OrderItem, Table
from inventory.models import Ingredient

def dashboard(request):
    # Get month string from query param or default to current month
    month_str = request.GET.get('month')
    if month_str:
        try:
            selected_date = datetime.strptime(month_str, '%Y-%m')
        except ValueError:
            selected_date = datetime.today()
    else:
        selected_date = datetime.today()

    # First and last day of the selected month
    start_of_month = selected_date.replace(day=1).date()
    if selected_date.month == 12:
        end_of_month = selected_date.replace(year=selected_date.year + 1, month=1, day=1).date() - timedelta(days=1)
    else:
        end_of_month = selected_date.replace(month=selected_date.month + 1, day=1).date() - timedelta(days=1)

    # Filter orders within the selected month
    orders = Order.objects.filter(created_at__date__range=(start_of_month, end_of_month))

    # --- Daily Summary ---
    daily_summary = defaultdict(lambda: {'sales': 0, 'orders': 0})
    for order in orders:
        order_date = order.created_at.date()
        daily_summary[order_date]['sales'] += order.get_total_price()
        daily_summary[order_date]['orders'] += 1

    for day_data in daily_summary.values():
        orders_count = day_data['orders']
        day_data['avg_order'] = day_data['sales'] / orders_count if orders_count > 0 else 0

    # --- Top-Selling Items in Month ---
    top_items = (
        OrderItem.objects.filter(order__created_at__range=(start_of_month, end_of_month))
        .values('menu_item__name')
        .annotate(quantity_sold=Sum('quantity'), total_revenue=Sum('line_total'))
        .order_by('-quantity_sold')[:5]
    )

    # --- Table Usage Summary for Month ---
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
        'daily_summary': sorted(daily_summary.items()),  # list of tuples: (date, data)
        'top_items': top_items,
        'table_data': table_data,
        'low_stock_ingredients': low_stock_ingredients,
    }

    return render(request, 'center/dashboard.html', context)
