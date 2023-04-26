from decimal import Decimal

from rest_framework import serializers

from coupons.models import Coupon
from orders.models import Order, OrderItem
from products.serializers import ProductSerializer
from users.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sub_total = serializers.SerializerMethodField(method_name='total')

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'price', 'quantity', 'sub_total')

    def total(self, order_item=OrderItem):
        return order_item.quantity * order_item.price


class OrderSerializer(serializers.ModelSerializer):
    coupon = serializers.SlugRelatedField(
        queryset=Coupon.objects.all(),
        slug_field='code'
    )
    items = OrderItemSerializer(many=True)

    initiator = UserSerializer()

    grand_total = serializers.SerializerMethodField(method_name='main_total')

    class Meta:
        model = Order
        fields = (
            'id', 'status', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'postal_code', 'city',
            'created',
            'updated', 'payment_id', 'initiator', 'coupon', 'discount', 'items', 'grand_total')

    def main_total(self, order=Order):
        total_cost = sum(item.get_cost() for item in OrderItem.objects.filter(order=order))
        total = total_cost - total_cost * (Order.objects.get(id=order.id).discount / Decimal('100'))
        return total
