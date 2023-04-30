from django.urls import path

from .views import AboutView, ContactView, IndexView, ShippingAndPaymentView, PrivacyPolicyView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about'),
    path('shipping_and_payment/', ShippingAndPaymentView.as_view(), name='shipping_and_payment'),
    path('privacy_policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
]
