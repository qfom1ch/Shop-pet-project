from .cart import Cart


def cart(request):
    """Returns a request with the functionality of the cart."""
    return {'cart': Cart(request)}
