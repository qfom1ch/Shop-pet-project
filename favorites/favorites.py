import copy

from django.conf import settings

from products.models import Product


class Favorites(object):

    def __init__(self, request):
        """
        Initializing the favorites.
        """
        self.session = request.session
        favorites = self.session.get(settings.FAVORITES_SESSION_ID)
        if not favorites:
            favorites = self.session[settings.FAVORITES_SESSION_ID] = {}
        self.favorites = favorites

    def add(self, product):
        """
        Add a product to the favorites.
        """
        product_id = str(product.id)
        if product_id not in self.favorites:
            self.favorites[product_id] = {
                'price': str(product.price)}
        self.save()

    def save(self):
        """
        Saving a session and marks the session as "modified" to make sure it's saved.
        """
        self.session[settings.FAVORITES_SESSION_ID] = self.favorites
        self.session.modified = True

    def remove(self, product):
        """
        Removing an item from the favorites.
        """
        product_id = str(product.id)
        if product_id in self.favorites:
            del self.favorites[product_id]
            self.save()

    def __iter__(self):
        """
        Iterating through the items in the favorites and getting the products from the database.
        """
        product_ids = self.favorites.keys()
        products = Product.objects.filter(id__in=product_ids)
        favorites = copy.deepcopy(self.favorites)
        for product in products:
            favorites[str(product.id)]['product'] = product

        for item in favorites.values():
            yield item

    def __len__(self):
        """
        Counting all items in the favorites.
        """
        return len(self.favorites)

    def clear(self):
        """
        Removing a favorites from a session.
        """
        del self.session[settings.FAVORITES_SESSION_ID]
        self.session.modified = True
