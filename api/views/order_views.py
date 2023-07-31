from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.select_related('initiator', 'coupon').prefetch_related('items__product__category')
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        queryset = super(OrderModelViewSet, self).get_queryset()
        return queryset.filter(initiator=self.request.user)
