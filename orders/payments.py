import uuid
from django.views.generic.base import View
from yookassa import Configuration, Payment

Configuration.account_id = '213661'
Configuration.secret_key = 'test_ktnN7ybTQgg1dxXcttLfFIF8cYLWdNDeK8UYRnJGJyc'
from orders.models import Order

class YandexPayment(View):

    def get(self, request):
        payment = Payment.create({
            "amount": {
                "value": "100.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://www.example.com/return_url"
            },
            "capture": True,
            "description": "Заказ №1"
        }, uuid.uuid4())



