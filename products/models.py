from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=128, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=128, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    MainImage = models.ImageField(upload_to='Main_products_images', blank=True, verbose_name='Главное изображение')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(to=Product, default=None, related_name='images', verbose_name='Товар',
                                on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_images', blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


# from shop.wsgi import *
# from products.models import ProductCategory

# python3 manage.py dumpdata products.ProductCategory > categories.json
# python3 manage.py loaddata products/fixtures/categories.json
