from django.shortcuts import render
import yaml

# get all products from my yaml
with open('static/site_data/products_data.yaml', 'r') as file:
    products_data = yaml.safe_load(file)

def all_products():
    output = []
    product_id = 1
    for category, items in products_data.get('categories', {}).items():
        for name, details in items.items():
            output.append({
                'id': product_id,
                'name': name,
                'price': details.get('price', 0),
                'category': category,
                'in_stock': True,
                'description': details.get('info', 'No description available.'),
            })
            product_id += 1
    return output

# all views
def home(request):
    all_items = all_products()

    featured_names = {'ChompStars', 'SlimTail Mix', 'RootSnax'}
    featured = [p for p in all_items if p['name'] in featured_names]

    context = {
        'title': 'Home - Soma Animals',
        'page_name': 'Homepage',
        'featured_products': featured,
    }
    return render(request, 'home.html', context)


def catalog(request):
    context = {
        'title': 'Catalog - Soma Animals',
        'page_name': 'Product Catalog',
        'categories': products_data['categories'].keys(),
        'products': all_products(),
    }
    return render(request, 'catalog.html', context)

def product_detail(request, product_id):
    all_p = all_products()
    product = next((p for p in all_p if p['id'] == product_id), None)

    if not product:
        return render(request, '404.html', status=404)

    context = {
        'title': f'{product["name"]} - Soma Animals',
        'page_name': product['name'],
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


from django.shortcuts import render

def about(request):
    context = {
        'title': 'About Us - Soma Animals',
        'page_name': 'About Us',
        'company_info': {
            'established': 2025,
            'locations': 1,
            'products_count': 20,
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
