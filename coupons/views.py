from django.contrib.messages.views import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from .models import Coupon, UsersUsedCoupon


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
                user_used = UsersUsedCoupon(user=request.user, coupon=coupon)
                user_used.save()
                message = 'Промокод успешно применен'
                messages.error(request, message)
                request.session['coupon_id'] = coupon.id
        except ObjectDoesNotExist:
            request.session['coupon_id'] = None
            message = 'Неверный промокод'
            messages.error(request, message)
    return redirect('cart:cart_detail')
