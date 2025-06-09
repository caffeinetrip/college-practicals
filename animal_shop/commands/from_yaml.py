import yaml
from ..models import Category, Product

with open("static/site_data/products_data.yaml", "r") as file:
    data = yaml.safe_load(file)

for category_name, items in data.get("categories", {}).items():
    category, _ = Category.objects.get_or_create(name=category_name)

    for product_name, details in items.items():
        Product.objects.update_or_create(
            name=product_name,
            category=category,
            defaults={
                "description": details.get("info", "No description available."),
                "price": details.get("price", 0.00),
                "is_visible": True,
            }
        )
