from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Код')
    valid_from = models.DateTimeField(verbose_name='Действует от')
    valid_to = models.DateTimeField(verbose_name='Действует до')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Скидка')
    active = models.BooleanField(verbose_name='Активация')
    user_used_coupon = models.ManyToManyField(to=User, through='UsersUsedCoupon',
                                              verbose_name='Пользователи использовавшие купон')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'


class UsersUsedCoupon(models.Model):
    coupon = models.ForeignKey(to=Coupon, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Купон')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
