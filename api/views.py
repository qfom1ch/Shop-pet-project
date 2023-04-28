from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cart.models import Cart
from cart.serializers import CartSerializer
from favorites.models import Favorites
from favorites.serializers import FavoritesSerializer
from orders.models import Order
from orders.serializers import OrderSerializer
from products.models import Product, ProductCategory
from products.serializers import CategorySerializer, ProductSerializer
from reviews.models import Reviews
from reviews.serializers import ReviewsSerializer
from users.models import User
from users.serializers import UserRegistrationSerializer, UserSerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ('create', 'destroy', 'update'):
            self.permission_classes = (IsAdminUser,)
        return super(CategoryModelViewSet, self).get_permissions()


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('create', 'destroy', 'update'):
            self.permission_classes = (IsAdminUser,)
        return super(ProductModelViewSet, self).get_permissions()


class CartModelViewSet(ModelViewSet):
    queryset = Cart.objects.all()
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
                return Response({'product_id': f'Нет продукта с id {product_id}'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Cart.create_or_update(products.first().id, self.request.user, quantity, coupon_code)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)

            return Response(serializer.data, status_code)
        except KeyError:
            return Response({'product_id': 'обязательное поле.'}, status=status.HTTP_400_BAD_REQUEST)


class FavoritesModelViewSet(ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = super(FavoritesModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product_id': f'Нет продукта с id {product_id}'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Favorites.create_or_update(products.first().id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status_code)
        except KeyError:
            return Response({'product_id': 'обязательное поле.'}, status=status.HTTP_400_BAD_REQUEST)


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_queryset(self):
        queryset = super(OrderModelViewSet, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class ReviewsModelViewSet(ModelViewSet):
    queryset = Reviews.objects.all()
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
            return Response({'rating': 'обязательное поле.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            text = request.data['text']
        except KeyError:
            return Response({'text': 'обязательное поле.'}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({'product_id': 'обязательное поле.'}, status=status.HTTP_400_BAD_REQUEST)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (IsAdminUser,)


class RegistrUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)
