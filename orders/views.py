import json
import uuid

from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from yookassa import Configuration, Payment
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import (WebhookNotificationEventType,
                                          WebhookNotificationFactory)

from cart.cart import Cart
from cart.models import Session
from common.views import TitleMixin
from orders.models import Order
from shop.settings import YANDEX_SECRET_KEY, YANDEX_SHOP_ID

from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import send_mail_about_order
from .utils import (get_client_ip, get_descriptions_for_payment,
                    quantity_minus_order_quantity)


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Shop - Спасибо за заказ!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Shop - Заказы'
    ordering = ('-created')

    def get_queryset(self):
        queryset = Order.objects.prefetch_related('items').filter(initiator=self.request.user)
        return queryset


class OrderDetail(TitleMixin, DetailView):
    model = Order
    queryset = Order.objects.select_related('coupon')
    template_name = 'orders/order.html'
    context_object_name = 'order'
    title = 'Shop - Информация о заказе'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.select_related('product').filter(order=self.kwargs.get('pk'))
        return context


def order_create(request):
    """Creates a payment page for the user and creates an order in the database after that clears the user's cart"""
    cart = Cart(request)
    Configuration.account_id = YANDEX_SHOP_ID
    Configuration.secret_key = YANDEX_SECRET_KEY
    description = get_descriptions_for_payment([(item['product'].name, item['quantity']) for item in cart])

    if request.method == 'POST':
        payment = Payment.create({
            "amount": {
                "value": f'{cart.get_total_price_after_discount()}',
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://010d-178-159-54-151.ngrok-free.app/orders/order-success/"
                # "return_url": "http://mysite.com:8443/orders/order-success/"
            },
            "capture": True,
            "description": f"{description}"
        }, uuid.uuid4())

        form = OrderCreateForm(request.POST)
        if form.is_valid():
            form.instance.initiator = request.user
            form.instance.payment_id = payment.id
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount

                session = Session(session_key=request.session.session_key, payment_id=payment.id)
                session.save()

            order.save()
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
    """Receives notification from yookassa and updates order details"""
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

            session = Session.objects.get(payment_id=payment_id)
            session_user = SessionStore(session_key=session.session_key)
            session_user['coupon_id'] = None
            session_user.save()
            session.delete()

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
