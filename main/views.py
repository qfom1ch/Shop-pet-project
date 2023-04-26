from django.views.generic.base import TemplateView

from common.views import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name = 'main/index.html'
    title = 'Shop'


class ContactView(TitleMixin, TemplateView):
    template_name = 'main/contact.html'
    title = 'Shop - Контакты'


class AboutView(TitleMixin, TemplateView):
    template_name = 'main/about.html'
    title = 'Shop - О нас'


class ShippingAndPaymentView(TitleMixin, TemplateView):
    template_name = 'main/shipping_and_payment.html'
    title = 'Shop - Доставка и оплата'
