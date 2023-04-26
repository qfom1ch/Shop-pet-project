from django.contrib import admin

from .models import Coupon, UsersUsedCoupon


class UsersUsedCouponInline(admin.TabularInline):
    model = UsersUsedCoupon
    extra = 0


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    inlines = [UsersUsedCouponInline]
    search_fields = ['code']
