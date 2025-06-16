from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Category, Comment, Order, OrderItem
from .forms import CommentForm, OrderForm


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


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)

        if not product.in_stock:
            messages.error(request, f'{product.name} is currently out of stock.')
            return redirect('product_detail', product_id=product_id)

        quantity = int(request.POST.get('quantity', 1))

        cart = request.session.get('cart', {})

        product_id_str = str(product_id)
        if product_id_str in cart:
            cart[product_id_str]['quantity'] += quantity
        else:
            cart[product_id_str] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': quantity,
                'image_url': product.image.url if product.image else None
            }

        request.session['cart'] = cart
        request.session.modified = True

        messages.success(request, f'{product.name} has been added to your cart.')
        return redirect('cart')

    return redirect('catalog')


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(pk=product_id)
            item_total = float(item_data['price']) * item_data['quantity']
            cart_items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'price': float(item_data['price']),
                'total': item_total
            })
            total_price += item_total
        except Product.DoesNotExist:
            continue

    context = {
        'title': 'Cart - Soma Animals',
        'page_name': 'Your Cart',
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': sum(item['quantity'] for item in cart.values())
    }
    return render(request, 'cart.html', context)


def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)

        if product_id_str in cart:
            new_quantity = int(request.POST.get('quantity', 1))
            if new_quantity > 0:
                cart[product_id_str]['quantity'] = new_quantity
            else:
                del cart[product_id_str]

            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, 'Cart updated successfully.')

    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        product_name = cart[product_id_str]['name']
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'{product_name} has been removed from your cart.')

    return redirect('cart')


def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    cart_items = []
    total_amount = 0

    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(pk=product_id)
            item_total = float(item_data['price']) * item_data['quantity']
            cart_items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'price': float(item_data['price']),
                'total': item_total
            })
            total_amount += item_total
        except Product.DoesNotExist:
            continue

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_amount = total_amount
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            request.session['cart'] = {}
            request.session.modified = True

            messages.success(request, f'Order #{order.pk} has been placed successfully!')
            return redirect('order_confirmation', order_id=order.pk)
    else:
        form = OrderForm()

    context = {
        'title': 'Checkout - Soma Animals',
        'page_name': 'Checkout',
        'form': form,
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'checkout.html', context)


def order_confirmation(request, order_id):

    order = get_object_or_404(Order, pk=order_id)

    context = {
        'title': 'Order Confirmation - Soma Animals',
        'page_name': 'Order Confirmation',
        'order': order,
    }
    return render(request, 'order_confirmation.html', context)


def about(request):
    context = {
        'title': 'About Us - Soma Animals',
        'page_name': 'About Us',
        'company_info': {
            "established": 2025,
            "locations": 1,
            "products_count": Product.objects.count(),
            "description": (
                "At Soma Animals, we don't just feed pets — we transform them."
            "Since 2010, we've explored the boundaries of nutrition, magic, and memory, crafting treats that glow, whisper, and occasionally disappear."
            "From dream-fed jerky to sentient loaves, our products are designed not only to nourish but to bewilder and delight. "
            "With a catalog of over 5,000 unconventional formulas sourced from ethical dimensions, "
            "our pharmacists work tirelessly across 5 locations to bring pets everything they never knew they craved.\n\n"
            "Trust Soma Animals — because ordinary food is for ordinary creatures."
            )
        }
    }
    return render(request, 'about.html', context)