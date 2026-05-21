from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, CartItem


def get_or_create_cart(request):
    """Get or create a cart for the current user/session."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_detail(request):
    """Display the shopping cart."""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product', 'product__category')
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    """Add a product to the cart."""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        quantity = 1

    # Check stock availability
    if quantity > product.stock_quantity:
        messages.error(request, f'Only {product.stock_quantity} units of "{product.name}" available.')
        return redirect('products:product_detail', slug=product.slug)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock_quantity:
            messages.error(request, f'Cannot add more. Only {product.stock_quantity} units available (you have {cart_item.quantity} in cart).')
            return redirect('cart:cart_detail')
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f'Updated "{product.name}" quantity to {cart_item.quantity}.')
    else:
        messages.success(request, f'Added "{product.name}" to your cart.')

    # Redirect back to where the user came from, or cart
    next_url = request.POST.get('next', '')
    if next_url:
        return redirect(next_url)
    return redirect('cart:cart_detail')


@require_POST
def update_cart_item(request, item_id):
    """Update the quantity of a cart item."""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        cart_item.delete()
        messages.success(request, f'Removed "{cart_item.product.name}" from your cart.')
    elif quantity > cart_item.product.stock_quantity:
        messages.error(request, f'Only {cart_item.product.stock_quantity} units of "{cart_item.product.name}" available.')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'Updated "{cart_item.product.name}" quantity to {quantity}.')

    return redirect('cart:cart_detail')


@require_POST
def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Removed "{product_name}" from your cart.')
    return redirect('cart:cart_detail')


@require_POST
def clear_cart(request):
    """Remove all items from the cart."""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, 'Your cart has been cleared.')
    return redirect('cart:cart_detail')
