from django.contrib import admin
from .models import Order, OrderItem



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['initiator', 'id', 'status', 'first_name', 'last_name', 'phone_number', 'email',
                    'city', 'address', 'postal_code',
                    'created', 'updated']
    list_filter = ['status', 'created', 'updated']
    inlines = [OrderItemInline]

