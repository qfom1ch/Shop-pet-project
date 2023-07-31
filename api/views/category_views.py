from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from products.models import ProductCategory
from products.serializers import CategorySerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ('create', 'destroy', 'update'):
            self.permission_classes = (IsAdminUser,)
        return super(CategoryModelViewSet, self).get_permissions()
