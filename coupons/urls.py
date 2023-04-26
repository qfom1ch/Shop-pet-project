from django.urls import path

from .views import coupon_apply

app_name = 'coupons'

urlpatterns = [
    path('coupon_apply/', coupon_apply, name='coupon_apply'),
]
