from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category name")
    description = models.TextField(blank=True, verbose_name="Category description")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_TYPES = [
        ('treats', 'Treats'),
        ('diet', 'Diet'),
        ('organic', 'Organic'),
        ('supplements', 'Supplements'),
    ]

    COUNTRY_CHOICES = [
        ('UA', 'Ukraine'),
        ('US', 'USA'),
        ('PL', 'Polish'),
    ]

    STOCK_STATUS = [
        ('in_stock', 'In stock'),
        ('out_of_stock', 'Out of stock'),
        ('limited', 'Limited'),
        ('pre_order', 'Pre order'),
    ]

    name = models.CharField(max_length=200, verbose_name="Name")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Price"
    )
    manufacturer = models.CharField(
        max_length=100,
        default="Unknown",
        verbose_name='Manufacturer'
    )
    country = models.CharField(
        max_length=2,
        choices=COUNTRY_CHOICES,
        default='UA',
        verbose_name="Country"
    )
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPES,
        default='treats',
        verbose_name="Product Type"
    )
    stock_status = models.CharField(
        max_length=20,
        choices=STOCK_STATUS,
        default='in_stock',
        verbose_name="Stock Status"
    )
    package = models.CharField(
        max_length=100,
        blank=True,
        default="1 package",
        verbose_name="Package"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
        verbose_name="Rating (1-5)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Create Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update Date")
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name="Save product")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - £{self.price}"

    @property
    def in_stock(self):
        return self.stock_status == 'in_stock'

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])

    def get_stock_display_color(self):
        colors = {
            'in_stock': 'green',
            'out_of_stock': 'red',
            'limited': 'orange',
            'pre_order': 'blue',
        }
        return colors.get(self.stock_status, 'gray')

class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=100, verbose_name="Client Name")
    customer_phone = models.CharField(max_length=20, verbose_name="Phone Number")
    customer_email = models.EmailField(blank=True, verbose_name="Email")
    delivery_address = models.TextField(verbose_name="Delivery Address")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Delivery Status"
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Total Amount"
    )
    notes = models.TextField(blank=True, verbose_name="Notes")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Create Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "Delivery Order"
        verbose_name_plural = "Delivery Orders"
        ordering = ['-created_at']

    def __str__(self):
        return f"Delivery #{self.pk} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price per unit")

    class Meta:
        verbose_name = "Delivery Order Item"
        verbose_name_plural = "Delivery Order Items"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.price