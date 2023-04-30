from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from coupons.models import Coupon
from products.models import Product
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    CANCELED = 4
    REFUND_SUCCEEDED = 5

    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
        (CANCELED, 'Отменен'),
        (REFUND_SUCCEEDED, 'Успешный возврат'),
    )

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Эл. почта')
    phone_number = models.CharField(max_length=50, verbose_name='Тел. номер')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс')
    city = models.CharField(max_length=100, verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES, verbose_name='Статус')
    payment_id = models.CharField(max_length=128, blank=True, null=True, verbose_name='Идентификатор платежа')
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Инициатор')
    coupon = models.ForeignKey(to=Coupon, on_delete=models.CASCADE,
                               null=True,
                               blank=True, verbose_name='Купон')
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)], verbose_name='Скидка')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        """Returns the total price of the order with a discount if it was applied."""
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        """Returns the price of a product given its quantity."""
        return self.price * self.quantity

# from shop.wsgi import *
