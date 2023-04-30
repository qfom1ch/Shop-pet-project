import copy
from decimal import Decimal

from django.conf import settings

from coupons.models import Coupon
from products.models import Product


class Cart(object):

    def __init__(self, request):
        """
        Initializing the cart.
        """
        self.session = request.session  # request.session.get('coupon_id')
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            if quantity > product.quantity:
                quantity = product.quantity
            self.cart[product_id]['quantity'] = quantity
        else:
            if self.cart[product_id]['quantity'] + quantity > product.quantity:
                self.cart[product_id]['quantity'] = product.quantity
            else:
                self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Saving a session and marks the session as "modified" to make sure it's saved.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """
        Removing an item from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterating through the items in the cart and getting the products from the database.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = copy.deepcopy(self.cart)
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Counting all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the cost of items in the shopping cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        """
        Removing a cart from a session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    @property
    def coupon(self):
        """
        Checks if there is a coupon in the session and returns it, if not returns None.
        """
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        """
        Calculation of the amount of the discount.
        """
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        """
        Calculation of the final price after the discount.
        """
        return self.get_total_price() - self.get_discount()
