from statistics import fmean

from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Категория')
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the full url of the category"""
        return reverse('products:category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=128, unique=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    short_description = models.TextField(blank=True, null=True, verbose_name='Краткое описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    MainImage = models.ImageField(upload_to='Main_products_images', blank=True, null=True,
                                  verbose_name='Главное изображение')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the full url of the category"""
        return reverse('products:product_detail', args=[self.slug])

    def get_review_count(self):
        """Returns all comments for a specific product"""
        return self.reviews_set.count()

    def get_review_with_users(self):
        """Returns all comments join with users for a specific product"""
        return self.reviews_set.select_related('user').only('user__username', 'user__image', 'text', 'image', 'rating',
                                                            'product')

    def get_avg_rating(self):
        """Calculates the average rating of a product"""
        ratings = self.reviews_set.all().values_list('rating', flat=True)
        if len(ratings) > 0:
            avg_rating = round(fmean(ratings))
        else:
            avg_rating = 0
        return avg_rating


class ProductImage(models.Model):
    product = models.ForeignKey(to=Product, default=None, related_name='images', verbose_name='Товар',
                                on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_images', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
