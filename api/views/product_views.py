from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.serializers import ProductSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('create', 'destroy', 'update'):
            self.permission_classes = (IsAdminUser,)
        return super(ProductModelViewSet, self).get_permissions()
