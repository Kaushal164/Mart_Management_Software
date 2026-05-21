from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, F, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from datetime import timedelta
from products.models import Product, Category, StockMovement
from orders.models import Order, OrderItem
from django.contrib.auth.models import User


def staff_required(view_func):
    """Decorator to require staff access."""
    decorated_view = user_passes_test(lambda u: u.is_staff, login_url='accounts:login')(view_func)
    return login_required(decorated_view)


@staff_required
def index(request):
    """Main dashboard with overview stats."""
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    last_7_days = today - timedelta(days=7)

    # Overall stats
    total_products = Product.objects.filter(is_active=True).count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(
        status__in=['confirmed', 'completed']
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    total_customers = User.objects.filter(is_staff=False).count()

    # Today's stats
    today_orders = Order.objects.filter(created_at__date=today)
    today_revenue = today_orders.filter(
        status__in=['confirmed', 'completed']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    today_order_count = today_orders.count()

    # Last 7 days revenue
    week_revenue = Order.objects.filter(
        created_at__date__gte=last_7_days,
        status__in=['confirmed', 'completed']
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Low stock products
    low_stock_products = Product.objects.filter(
        is_active=True,
        stock_quantity__lte=F('minimum_stock')
    ).order_by('stock_quantity')[:10]

    # Recent orders
    recent_orders = Order.objects.order_by('-created_at')[:10]

    # Top selling products (last 30 days)
    top_products = OrderItem.objects.filter(
        order__created_at__date__gte=last_30_days,
        order__status__in=['confirmed', 'completed']
    ).values('product_name').annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum('total_price')
    ).order_by('-total_sold')[:10]

    # Daily revenue for chart (last 7 days)
    daily_revenue = Order.objects.filter(
        created_at__date__gte=last_7_days,
        status__in=['confirmed', 'completed']
    ).annotate(date=TruncDate('created_at')).values('date').annotate(
        revenue=Sum('total_amount'),
        orders=Count('id')
    ).order_by('date')

    # Order status breakdown
    order_status_counts = Order.objects.values('status').annotate(count=Count('id'))

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'today_revenue': today_revenue,
        'today_order_count': today_order_count,
        'week_revenue': week_revenue,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'daily_revenue': list(daily_revenue),
        'order_status_counts': order_status_counts,
    }
    return render(request, 'dashboard/index.html', context)


@staff_required
def inventory(request):
    """Inventory management page."""
    products = Product.objects.filter(is_active=True).select_related('category').order_by('stock_quantity')

    # Filter by stock status
    stock_filter = request.GET.get('stock', '')
    if stock_filter == 'low':
        products = products.filter(stock_quantity__lte=F('minimum_stock'))
    elif stock_filter == 'out':
        products = products.filter(stock_quantity=0)

    # Search
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(sku__icontains=query)
        )

    context = {
        'products': products,
        'stock_filter': stock_filter,
        'query': query,
        'total_products': Product.objects.filter(is_active=True).count(),
        'low_stock_count': Product.objects.filter(is_active=True, stock_quantity__lte=F('minimum_stock')).count(),
        'out_of_stock_count': Product.objects.filter(is_active=True, stock_quantity=0).count(),
    }
    return render(request, 'dashboard/inventory.html', context)


@staff_required
def update_stock(request, product_id):
    """Update stock for a product."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', 0))
        notes = request.POST.get('notes', '')

        if quantity <= 0:
            messages.error(request, 'Quantity must be greater than zero.')
            return redirect('dashboard:inventory')

        if action == 'add':
            product.stock_quantity += quantity
            product.save()
            StockMovement.objects.create(
                product=product,
                movement_type='in',
                quantity=quantity,
                reference='Manual Stock Add',
                notes=notes,
            )
            messages.success(request, f'Added {quantity} units to "{product.name}". New stock: {product.stock_quantity}')
        elif action == 'remove':
            if quantity > product.stock_quantity:
                messages.error(request, f'Cannot remove {quantity} units. Only {product.stock_quantity} in stock.')
                return redirect('dashboard:inventory')
            product.stock_quantity -= quantity
            product.save()
            StockMovement.objects.create(
                product=product,
                movement_type='out',
                quantity=quantity,
                reference='Manual Stock Remove',
                notes=notes,
            )
            messages.success(request, f'Removed {quantity} units from "{product.name}". New stock: {product.stock_quantity}')
        elif action == 'set':
            old_qty = product.stock_quantity
            product.stock_quantity = quantity
            product.save()
            StockMovement.objects.create(
                product=product,
                movement_type='adjustment',
                quantity=quantity - old_qty,
                reference='Stock Adjustment',
                notes=notes or f'Adjusted from {old_qty} to {quantity}',
            )
            messages.success(request, f'Stock for "{product.name}" set to {quantity}.')

    return redirect('dashboard:inventory')


@staff_required
def sales_report(request):
    """Sales report with date filtering."""
    today = timezone.now().date()
    start_date = request.GET.get('start_date', (today - timedelta(days=30)).isoformat())
    end_date = request.GET.get('end_date', today.isoformat())

    orders = Order.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date,
        status__in=['confirmed', 'completed']
    )

    total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    total_orders = orders.count()
    total_items_sold = OrderItem.objects.filter(order__in=orders).aggregate(total=Sum('quantity'))['total'] or 0
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    # Daily breakdown
    daily_sales = orders.annotate(date=TruncDate('created_at')).values('date').annotate(
        revenue=Sum('total_amount'),
        orders=Count('id'),
        items=Sum('items__quantity')
    ).order_by('-date')

    # Top products in period
    top_products = OrderItem.objects.filter(order__in=orders).values(
        'product_name'
    ).annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum('total_price')
    ).order_by('-total_revenue')[:20]

    # Payment method breakdown
    payment_breakdown = orders.values('payment_method').annotate(
        count=Count('id'),
        total=Sum('total_amount')
    )

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_items_sold': total_items_sold,
        'avg_order_value': avg_order_value,
        'daily_sales': daily_sales,
        'top_products': top_products,
        'payment_breakdown': payment_breakdown,
    }
    return render(request, 'dashboard/sales_report.html', context)


@staff_required
def order_management(request):
    """Manage all orders."""
    orders = Order.objects.all().order_by('-created_at')

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)

    # Search
    query = request.GET.get('q', '')
    if query:
        orders = orders.filter(
            Q(order_number__icontains=query) |
            Q(customer_name__icontains=query) |
            Q(customer_phone__icontains=query)
        )

    context = {
        'orders': orders,
        'status_filter': status_filter,
        'query': query,
    }
    return render(request, 'dashboard/order_management.html', context)


@staff_required
def update_order_status(request, order_id):
    """Update order status."""
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        payment_status = request.POST.get('payment_status')

        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
        if payment_status in dict(Order.PAYMENT_STATUS_CHOICES):
            order.payment_status = payment_status
        order.save()
        messages.success(request, f'Order #{order.order_number} updated successfully.')

    return redirect('dashboard:order_management')
