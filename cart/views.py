from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from coupons.forms import CouponApplyForm
from products.models import Product

from .cart import Cart
from .forms import (CartAddProductForm, CartAddProductFormQuantity,
                    CartAddProductFormWithoutChoice)


@require_POST
def cart_add(request, product_id):
    """Adds a product to the user's cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if CartAddProductForm(request.POST):
        form = CartAddProductForm(request.POST)
    else:
        form = CartAddProductFormWithoutChoice(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    if form.cleaned_data['update'] is True:
        messages.success(request, 'Количество изменено')
    else:
        messages.success(request, 'Товар успешно добавлен в корзину')
    return redirect(request.META['HTTP_REFERER'])


def cart_remove(request, product_id):
    """Removes a product from the user's cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Returns the user's cart"""
    cart = Cart(request)
    cart_product_form_quantity = CartAddProductFormQuantity()
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/cart_detail.html', {'cart': cart,
                                                     'cart_product_form_quantity': cart_product_form_quantity,
                                                     'coupon_apply_form': coupon_apply_form,
                                                     'title': 'Shop - Корзина',
                                                     })
