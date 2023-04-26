from django.db import models

from products.models import Product
from users.models import User


class Reviews(models.Model):
    """Отзывы"""

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField("Сообщение", max_length=5000)
    product = models.ForeignKey(to=Product, verbose_name="товар", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Reviews_images', blank=True, null=True, verbose_name='Изображение')
    pub_date = models.DateTimeField('Дата комментария', auto_now_add=True)
    rating = models.PositiveIntegerField(blank=True, null=True, verbose_name='Рейтинг')

    def __str__(self):
        return f'{self.user.username} - {self.product}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    @classmethod
    def create_or_update(cls, product_id, user, text, rating):
        if rating is not None:
            obj = Reviews.objects.create(user=user, product_id=product_id, text=text, rating=rating)
        else:
            obj = Reviews.objects.create(user=user, product_id=product_id, text=text)
        return obj
