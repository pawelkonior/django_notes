from django.db import models
from django.utils.text import slugify


class ProductInStockQuerySet(models.QuerySet):
    def in_stock(self):
        return self.filter(stock_count__gt=0)


class Product(models.Model):
    name = models.CharField(max_length=100)  # <input type='text'>
    stock_count = models.IntegerField(help_text="How many items are currently in stock.")  # <input type='number'>
    price = models.DecimalField(max_digits=6, decimal_places=2)  # <input type='number'>
    description = models.TextField(default="", blank=True)  # <textarea></textarea>
    sku = models.CharField(verbose_name="Stock Keeping Unit", max_length=20, unique=True)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('price',)

    objects = models.Manager()
    in_stock = ProductInStockQuerySet.as_manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


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
        verbose_name_plural = 'Categories'
        ordering = ('name',)
