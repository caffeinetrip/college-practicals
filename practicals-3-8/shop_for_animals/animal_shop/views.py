from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Category, Comment
from .forms import CommentForm

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
    categories = Category.objects.filter(is_active=True)

    category_id = request.GET.get('category')
    selected_category = None
    if category_id:
        try:
            selected_category = Category.objects.get(id=category_id, is_active=True)
            products = Product.objects.filter(category__id=category_id, category__is_active=True)
        except Category.DoesNotExist:
            products = Product.objects.filter(category__is_active=True)
    else:
        products = Product.objects.filter(category__is_active=True)

    context = {
        'title': 'Catalog - Soma Animals',
        'page_name': 'Product Catalog',
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    }
    return render(request, 'catalog.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    similar_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = CommentForm()

    comments = product.comments.order_by('-created_at')

    context = {
        'product': product,
        'similar_products': similar_products,
        'form': form,
        'comments': comments,
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