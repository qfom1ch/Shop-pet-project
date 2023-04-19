from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Coupon, UsersUsedCoupon
from .forms import CouponApplyForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages.views import messages
from orders.models import Order

# @require_POST
# def coupon_apply(request):
#     now = timezone.now()
#     form = CouponApplyForm(request.POST)
#     if form.is_valid():
#         code = form.cleaned_data['code']
#         try:
#             coupon = Coupon.objects.get(code__exact=code,
#                                         valid_from__lte=now,
#                                         valid_to__gte=now,
#                                         active=True)
#             request.session['coupon_id'] = coupon.id
#         except ObjectDoesNotExist:
#             request.session['coupon_id'] = None
#             message = 'Неверный промокод'
#             messages.error(request, message)
#     return redirect('cart:cart_detail')


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__exact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)

            user_used_coupon = Coupon.objects.filter(user_used_coupon=request.user, code=code)
            if user_used_coupon:
                message = 'Вы использовали этот промокод'
                messages.error(request, message)
                return redirect('cart:cart_detail')
            else:
                user_used=UsersUsedCoupon(user=request.user, coupon=coupon)
                user_used.save()
                message = 'Промокод успешно применен'
                messages.error(request, message)
                request.session['coupon_id'] = coupon.id
                session_key = request.session.session_key # 'r3vucib46heb2kj9z6r32u8rousj7t94'
                a=3
        except ObjectDoesNotExist:
            request.session['coupon_id'] = None
            message = 'Неверный промокод'
            messages.error(request, message)
    return redirect('cart:cart_detail')
