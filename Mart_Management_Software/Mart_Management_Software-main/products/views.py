from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category


def home(request):
    """Homepage with featured products and categories."""
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    categories = Category.objects.filter(is_active=True)
    latest_products = Product.objects.filter(is_active=True)[:12]
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
    }
    return render(request, 'products/home.html', context)


def product_list(request):
    """List all products with filtering and search."""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)

    # Search
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Price filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['price', '-price', 'name', '-name', '-created_at']:
        products = products.order_by(sort_by)

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
        'sort_by': sort_by,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """Product detail page."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


def category_detail(request, slug):
    """Products filtered by category."""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)

    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['price', '-price', 'name', '-name', '-created_at']:
        products = products.order_by(sort_by)

    context = {
        'category': category,
        'products': products,
        'sort_by': sort_by,
    }
    return render(request, 'products/category_detail.html', context)
