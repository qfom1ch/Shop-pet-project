from django.db import models

from products.models import Product
from users.models import User


class Favorites(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    @classmethod
    def create_or_update(cls, product_id, user):
        favorites = Favorites.objects.filter(user=user, product_id=product_id)

        if not favorites.exists():
            obj = Favorites.objects.create(user=user, product_id=product_id)
            is_created = True
            return obj, is_created
        else:
            favorites = favorites.first()
            is_created = False
            return favorites, is_created
