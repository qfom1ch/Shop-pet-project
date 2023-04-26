import copy

from django.conf import settings

from products.models import Product


class Favorites(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        favorites = self.session.get(settings.FAVORITES_SESSION_ID)
        if not favorites:
            # save an empty cart in the session
            favorites = self.session[settings.FAVORITES_SESSION_ID] = {}
        self.favorites = favorites

    def add(self, product):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.favorites:
            self.favorites[product_id] = {
                'price': str(product.price)}
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.FAVORITES_SESSION_ID] = self.favorites
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.favorites:
            del self.favorites[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.favorites.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        favorites = copy.deepcopy(self.favorites)
        for product in products:
            favorites[str(product.id)]['product'] = product

        for item in favorites.values():
            yield item

    def __len__(self):
        return len(self.favorites)

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.FAVORITES_SESSION_ID]
        self.session.modified = True
