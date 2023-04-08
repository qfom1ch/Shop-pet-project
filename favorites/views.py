from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .favorites import Favorites
from django.contrib import messages
from .forms import FavoritesAddProductForm


@require_POST
def favorites_add(request, product_id):
    favorites = Favorites(request)
    product = get_object_or_404(Product, id=product_id)
    form = FavoritesAddProductForm(request.POST)
    if form.is_valid():
        favorites.add(product=product)
        messages.success(request, f'Товар успешно добавлен в избранное')
    return redirect(request.META['HTTP_REFERER'])




def favorites_remove(request, product_id):
    favorites = Favorites(request)
    product = get_object_or_404(Product, id=product_id)
    favorites.remove(product)
    return redirect('favorites:favorites')

def favorites(request):
    favorites = Favorites(request)
    return render(request, 'favorites/favorites.html', {'favorites': favorites})
