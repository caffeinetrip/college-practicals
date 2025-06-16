from django.contrib import admin
from .models import Product, Category, Order, OrderItem, Comment
from django.utils.html import format_html
from django.urls import reverse

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('name', 'text', 'created_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'manufacturer', 'country', 'product_type', 'stock_status', 'rating')
    list_filter = ('category', 'country', 'product_type', 'stock_status', 'manufacturer', 'rating')
    search_fields = ('name', 'description', 'manufacturer')
    list_editable = ('price', 'stock_status', 'rating')
    inlines = [CommentInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'image')
        }),
        ('Product Details', {
            'fields': ('manufacturer', 'country', 'product_type', 'package')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_status', 'rating')
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price', 'total_price')
    readonly_fields = ('total_price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'customer_email', 'delivery_address', 'status', 'get_products', 'get_items_count', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'customer_email')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_phone', 'customer_email', 'delivery_address')
        }),
        ('Order Details', {
            'fields': ('status', 'total_amount', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def get_products(self, obj):
        items = obj.items.all()
        if not items:
            return "Немає товарів"

        products_list = []
        for item in items:
            product_url = reverse('admin:animal_shop_product_change', args=[item.product.pk])
            product_link = format_html(
                '<a href="{}" target="_blank">{}</a> x{}',
                product_url,
                item.product.name,
                item.quantity
            )
            products_list.append(product_link)

        if len(products_list) > 3:
            displayed_products = products_list[:3]
            remaining_count = len(products_list) - 3
            result = ", ".join(displayed_products) + f" та ще {remaining_count}..."
        else:
            result = ", ".join(products_list)

        return format_html(result)

    get_products.short_description = 'Товари'
    get_products.allow_tags = True

    def get_items_count(self, obj):
        return obj.items.count()

    get_items_count.short_description = 'Кількість позицій'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'text_preview', 'created_at')
    list_filter = ('created_at', 'product__category')
    search_fields = ('name', 'text', 'product__name')
    readonly_fields = ('created_at',)

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Comment Preview'