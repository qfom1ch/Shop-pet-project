from django.shortcuts import render
from common.views import TitleMixin
from django.views.generic.base import TemplateView

from django.views.generic.list import ListView
from orders.models import Order

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from shop.settings import YANDEX_SHOP_ID, YANDEX_SECRET_KEY
import uuid

from django.http import HttpResponseRedirect

import json
from django.http import HttpResponse
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from yookassa.domain.common import SecurityHelper
from django.views.decorators.csrf import csrf_exempt
from .utils import get_client_ip, get_descriptions, quantity_minus_order_quantity
from .tasks import send_mail_about_order

class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Shop - Спасибо за заказ!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Shop - Заказы'
    queryset = Order.objects.all()
    ordering = ('-created')

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'orders/order.html', {'order':order,
                                                 'order_items': order_items,
                                                 })



def order_create(request):
    cart = Cart(request)
    Configuration.account_id = YANDEX_SHOP_ID
    Configuration.secret_key = YANDEX_SECRET_KEY
    description = get_descriptions([(item['product'].name, item['quantity']) for item in cart])

    if request.method == 'POST':
        payment = Payment.create({
            "amount": {
                "value": f'{cart.get_total_price()}',
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "http://mysite.com:8443/orders/order-success/"
            },
            "capture": True,
            "description": f"{description}"
        }, uuid.uuid4())

        form = OrderCreateForm(request.POST)
        if form.is_valid():
            form.instance.initiator = request.user
            form.instance.payment_id = payment.id
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
        cart.clear()
        return HttpResponseRedirect(payment.confirmation.confirmation_url)
    else:
        form = OrderCreateForm
    return render(request, 'orders/order-create.html',
                  {'cart': cart, 'form': form})


@csrf_exempt
def my_webhook_handler(request):
    ip = get_client_ip(request)
    if not SecurityHelper().is_ip_trusted(ip):
        return HttpResponse(status=400)

    event_json = json.loads(request.body)
    try:
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            payment_id = response_object.id
            order = Order.objects.get(payment_id=payment_id)
            order.status = order.PAID
            order.save()
            quantity_minus_order_quantity(order)
            send_mail_about_order.delay(payment_id)


        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            order = Order.objects.get(payment_id=response_object.id)
            order.status = order.CANCELED
            order.save()

        elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
            order = Order.objects.get(payment_id=response_object.id)
            order.status = order.REFUND_SUCCEEDED
            order.save()

        else:
            return HttpResponse(status=400)

        Configuration.configure(YANDEX_SHOP_ID, YANDEX_SECRET_KEY)

    except Exception:
        return HttpResponse(status=400)

    return HttpResponse(status=200)
