from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from cart.views import get_or_create_cart
from products.models import Product, StockMovement
from .models import Order, OrderItem
from .forms import CheckoutForm


def checkout(request):
    """Checkout page - create an order from cart items."""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product')

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty. Add some items before checkout.')
        return redirect('cart:cart_detail')

    # Pre-fill form for authenticated users
    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'customer_name': request.user.get_full_name() or request.user.username,
            'customer_email': request.user.email,
        }
        if hasattr(request.user, 'profile'):
            initial_data['customer_phone'] = request.user.profile.phone
            initial_data['customer_address'] = request.user.profile.address

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create the order
                order = form.save(commit=False)
                if request.user.is_authenticated:
                    order.user = request.user
                order.save()

                # Create order items and update stock
                subtotal = 0
                for cart_item in cart_items:
                    product = cart_item.product

                    # Check stock availability
                    if cart_item.quantity > product.stock_quantity:
                        messages.error(request, f'"{product.name}" only has {product.stock_quantity} units available.')
                        return redirect('cart:cart_detail')

                    unit_price = product.effective_price
                    item_total = unit_price * cart_item.quantity

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        product_sku=product.sku,
                        quantity=cart_item.quantity,
                        unit_price=unit_price,
                        total_price=item_total,
                    )

                    # Reduce stock
                    product.stock_quantity -= cart_item.quantity
                    product.save()

                    # Record stock movement
                    StockMovement.objects.create(
                        product=product,
                        movement_type='out',
                        quantity=cart_item.quantity,
                        reference=f'Order #{order.order_number}',
                        notes=f'Sold via order {order.order_number}',
                    )

                    subtotal += item_total

                # Calculate totals
                order.subtotal = subtotal
                order.tax_amount = subtotal * 13 / 100  # 13% VAT
                order.total_amount = order.subtotal + order.tax_amount - order.discount_amount
                order.status = 'confirmed'
                order.save()

                # Clear the cart
                cart.items.all().delete()

                messages.success(request, f'Order #{order.order_number} placed successfully!')
                return redirect('orders:order_confirmation', order_number=order.order_number)
    else:
        form = CheckoutForm(initial=initial_data)

    # Calculate summary
    subtotal = cart.subtotal
    tax = subtotal * 13 / 100
    total = subtotal + tax

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)


def order_confirmation(request, order_number):
    """Order confirmation page after successful checkout."""
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'order': order,
    }
    return render(request, 'orders/order_confirmation.html', context)


@login_required
def order_list(request):
    """List all orders for the current user."""
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail(request, order_number):
    """Show details of a specific order."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)
