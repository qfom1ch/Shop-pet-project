from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Product
from reviews.models import Reviews
from reviews.serializers import ReviewsSerializer


class ReviewsModelViewSet(ModelViewSet):
    queryset = Reviews.objects.all()
    # don't pass tests with:
    # queryset = Reviews.objects.select_related('user', 'product__category')
    serializer_class = ReviewsSerializer

    def get_permissions(self):
        if self.action in ('create', 'destroy', 'update'):
            self.permission_classes = (IsAuthenticated,)
        return super(ReviewsModelViewSet, self).get_permissions()

    def get_queryset(self):
        queryset = super(ReviewsModelViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return queryset
        if self.action in ('destroy', 'update'):
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):

        try:
            rating = request.data['rating']
        except KeyError:
            return Response(
                {'product_id': 'обязательное поле.', 'text': 'обязательное поле.', 'rating': 'обязательное поле.'},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            text = request.data['text']
        except KeyError:
            return Response(
                {'product_id': 'обязательное поле.', 'text': 'обязательное поле.', 'rating': 'обязательное поле.'},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product_id': f'Нет продукта с id {product_id}'}, status=status.HTTP_400_BAD_REQUEST)
            obj = Reviews.create_or_update(products.first().id, self.request.user, text, rating)
            status_code = status.HTTP_201_CREATED
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status_code)
        except KeyError:
            return Response(
                {'product_id': 'обязательное поле.', 'text': 'обязательное поле.', 'rating': 'обязательное поле.'},
                status=status.HTTP_400_BAD_REQUEST)
