from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Category Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Product Name"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name=_("Category"))
    description = models.TextField(verbose_name=_("Description"))
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Price"))
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name=_("Product Image"))
    is_visible = models.BooleanField(default=True, verbose_name=_("Visible"))
    is_limited = models.BooleanField(default=False, verbose_name=_("Limited Edition"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.price} ₴)"

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.pk])