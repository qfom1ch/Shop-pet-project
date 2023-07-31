from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cart.models import Cart
from cart.serializers import CartSerializer
from products.models import Product


class CartModelViewSet(ModelViewSet):
    queryset = Cart.objects.select_related('user', 'product')
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = super(CartModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):

        try:
            coupon_code = request.data['coupon']
        except KeyError:
            coupon_code = None

        try:
            quantity = int(request.data['quantity'])
        except KeyError:
            quantity = 1

        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response(
                    {'product_id': f'Нет продукта с id {product_id}'},
                    status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Cart.create_or_update(products.first().id,
                                                    self.request.user,
                                                    quantity, coupon_code)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)

            return Response(serializer.data, status_code)
        except KeyError:
            return Response({'product_id': 'обязательное поле.'},
                            status=status.HTTP_400_BAD_REQUEST)
