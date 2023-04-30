from .favorites import Favorites


def favorites(request):
    """Returns a request with the functionality of the favorites."""
    return {'favorites': Favorites(request)}
