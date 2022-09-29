from decimal import Decimal

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.functional import cached_property


class ProductInStockQuerySet(models.QuerySet):
    def in_stock(self):
        return self.filter(stock_count__gt=0)


class Modified(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Product(Modified):
    name = models.CharField(max_length=100)  # <input type='text'>
    stock_count = models.IntegerField(help_text="How many items are currently in stock.")  # <input type='number'>
    price = models.DecimalField(max_digits=6, decimal_places=2)  # <input type='number'>
    description = models.TextField(default="", blank=True)  # <textarea></textarea>
    sku = models.CharField(verbose_name="Stock Keeping Unit", max_length=20, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    second_name = models.CharField(max_length=45)
    third_name = models.CharField(max_length=66, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('price',)
        constraints = [
            models.CheckConstraint(check=models.Q(price__gt=0), name="price_not_negative")
        ]

    objects = models.Manager()
    in_stock = ProductInStockQuerySet.as_manager()

    @cached_property
    def vat(self):
        return self.price * Decimal('0.23')

    def get_absolute_url(self):
        return reverse('store:product-detail', kwargs={'pk': self.pk})

    def get_canonical_url(self):
        pass

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


# class VirtualProduct(Product):
#     digital_version = models.CharField(max_length=200)
#
#
# class RealProduct(Product):
#     shipping_cost = models.DecimalField()


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_image')  # MIME TYPE, Pillow/PIL, Media setup, <input type='file'>
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return str(self.image)


class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField('Product', related_name='categories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Product Categories'
        verbose_name = 'Product Category'
        ordering = ('name',)
