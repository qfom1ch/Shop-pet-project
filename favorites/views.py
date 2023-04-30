from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product

from .favorites import Favorites
from .forms import FavoritesAddProductForm


@require_POST
def favorites_add(request, product_id):
    """
    Adds a product to the user's favorites and returns a message - 'Товар успешно добавлен в избранное'
    """
    favorites = Favorites(request)
    product = get_object_or_404(Product, id=product_id)
    form = FavoritesAddProductForm(request.POST)
    if form.is_valid():
        favorites.add(product=product)
        messages.success(request, 'Товар успешно добавлен в избранное')
    return redirect(request.META['HTTP_REFERER'])


def favorites_remove(request, product_id):
    """Removes a product from a favorite user."""
    favorites = Favorites(request)
    product = get_object_or_404(Product, id=product_id)
    favorites.remove(product)
    return redirect('favorites:favorites')


def favorites(request):
    """Returns the user's favorite products."""
    favorites = Favorites(request)
    return render(request, 'favorites/favorites.html', {'favorites': favorites,
                                                        'title': 'Shop - Избранное', })
