from django.shortcuts import render
from common.views import TitleMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from orders.models import Order

from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from shop.settings import YANDEX_SHOP_ID, YANDEX_SECRET_KEY
import uuid
from django.views.generic.base import View
from yookassa import Configuration, Payment
from django.http import HttpResponseRedirect



class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Shop - Спасибо за заказ!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = ('-created')

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Заказ #{self.object.id}'
        return context


# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             form.instance.initiator = request.user
#             order = form.save()
#             for item in cart:
#                 OrderItem.objects.create(order=order,
#                                          product=item['product'],
#                                          price=item['price'],
#                                          quantity=item['quantity'])
#             cart.clear()
#             return render(request, 'orders/success.html',
#                           {'order': order})
#     else:
#         form = OrderCreateForm
#     return render(request, 'orders/order-create.html',
#                   {'cart': cart, 'form': form})

Configuration.account_id = YANDEX_SHOP_ID
Configuration.secret_key = YANDEX_SECRET_KEY

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            form.instance.initiator = request.user
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            payment = Payment.create({
                "amount": {
                    "value": f'{cart.get_total_price()}',
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://www.example.com/return_url"  # сделать с ngrok  http://mysite.com:8000/orders/order-create/
                },
                "capture": True,
                "description": "Заказ №1"
            }, uuid.uuid4())

            cart.clear()
            return HttpResponseRedirect(payment.confirmation.confirmation_url)
    else:
        form = OrderCreateForm
    return render(request, 'orders/order-create.html',
                  {'cart': cart, 'form': form})