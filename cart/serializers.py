from rest_framework import fields, serializers

from cart.models import Cart
from products.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()
    coupon = serializers.CharField(required=False)

    class Meta:
        model = Cart
        fields = ('id', 'product', 'quantity', 'sum', 'coupon', 'total_sum', 'total_quantity', 'created_timestamp')
        read_only_fields = ('created_timestamp',)

    def get_total_sum(self, obj):
        return Cart.objects.filter(user=obj.user.id).get_total_price_after_discount()

    def get_total_quantity(self, obj):
        return Cart.objects.filter(user=obj.user.id).total_quantity()
