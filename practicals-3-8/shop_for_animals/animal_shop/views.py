from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    featured_names = {'ChompStars', 'BlankBites', 'RootSnax'}
    featured = Product.objects.filter(name__in=featured_names, stock_status='in_stock')

    context = {
        'title': 'Home - Soma Animals',
        'page_name': 'Homepage',
        'featured_products': featured,
    }
    return render(request, 'home.html', context)

def catalog(request):
    products = Product.objects.filter(category__is_active=True)
    categories = Category.objects.filter(is_active=True)

    context = {
        'title': 'Catalog - Soma Animals',
        'page_name': 'Product Catalog',
        'categories': categories,
        'products': products,
    }
    return render(request, 'catalog.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'title': f'{product.name} - Soma Animals',
        'page_name': product.name,
        'product': product,
    }
    return render(request, 'product_detail.html', context)

def cart(request):
    context = {
        'title': 'Cart - Soma Animals',
        'page_name': 'Your cart',
        'cart_items': [],
        'total_price': 0
    }
    return render(request, 'cart.html', context)

def about(request):
    context = {
        'title': 'About Us - Soma Animals',
        'page_name': 'About Us',
        'company_info': {
            'established': 2025,
            'locations': 1,
            'products_count': Product.objects.count(),
            'description': (
                'At Soma Animals, we don’t just feed pets — we transform them. '
                'Since 2010, we’ve explored the boundaries of nutrition, magic, and memory, crafting treats that glow, whisper, and occasionally disappear. '
                'From dream-fed jerky to sentient loaves, our products are designed not only to nourish but to bewilder and delight. '
                'With a catalog of over 5,000 unconventional formulas sourced from ethical dimensions, '
                'our pharmacists work tirelessly across 5 locations to bring pets everything they never knew they craved.\n\n'
                'Trust Soma Animals — because ordinary food is for ordinary creatures.'
            )
        }
    }
    return render(request, 'about.html', context)
