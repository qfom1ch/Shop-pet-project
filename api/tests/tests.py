from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

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

# Tests CategoryApi
# python3 manage.py dumpdata --exclude contenttypes -o db_fixtures.json

class CategoryApiTestCase(APITestCase):
    fixtures = ['db_fixtures.json']
    url = reverse('api:category-list')

    def test_get(self):
        response = self.client.get(self.url)
        serializer_data = CategorySerializer(ProductCategory.objects.all(), many=True).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

    def test_create_for_admin(self):
        token = Token.objects.get(user__username='AdminUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(self.url, data={'name': 'new_category'}, headers={'Authorization': 'Token ' + token.key})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_category = ProductCategory.objects.first()
        self.assertEqual(new_category.name, 'new_category')
        client.logout()

    def test_create_for_simple_user(self):
        token = Token.objects.get(user__username='SimpleUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(self.url, data={'name': 'new_category'}, headers={'Authorization': 'Token ' + token.key})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        client.logout()


# Tests ProductApi

class ProductApiTestCase(APITestCase):
    fixtures = ['db_fixtures.json']
    url = reverse('api:products-list')

    def test_get(self):
        response = self.client.get(self.url)
        serializer_data = ProductSerializer(Product.objects.all(), many=True).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data['results'])

    def test_create_for_admin(self):
        token = Token.objects.get(user__username='AdminUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(self.url, data={'name': 'new_product', 'price': 123, 'category': 'Интерьерные цветы'},
                               headers={'Authorization': 'Token ' + token.key})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_product = Product.objects.first()
        self.assertEqual(new_product.name, 'new_product')
        client.logout()

    def test_create_for_simple_user(self):
        token = Token.objects.get(user__username='SimpleUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(self.url, data={'name': 'new_product', 'price': 123, 'category': 'Интерьерные цветы'},
                               headers={'Authorization': 'Token ' + token.key})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        client.logout()


# Tests CartApi

class CartApiTestCase(APITestCase):
    fixtures = ['db_fixtures.json']
    url = reverse('api:cart-list')

    def test_get_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_authorized(self):
        token = Token.objects.get(user__username='SimpleUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(self.url)
        serializer_data = CartSerializer(Cart.objects.filter(user__username='SimpleUser'), many=True).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)
        client.logout()

    def test_create(self):
        token = Token.objects.get(user__username='SimpleUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(self.url, data={'product_id': 1},
                               headers={'Authorization': 'Token ' + token.key})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_product_in_cart = Cart.objects.filter(user__username='SimpleUser').first().product
        self.assertEqual(new_product_in_cart.name, Product.objects.get(id=1).name)
        client.logout()


# Tests FavoritesApi

class FavoritesApiTestCase(APITestCase):
    fixtures = ['db_fixtures.json']
    url = reverse('api:favorites-list')

    def test_get_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_authorized(self):
        token = Token.objects.get(user__username='SimpleUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(self.url)
        serializer_data = FavoritesSerializer(Favorites.objects.filter(user__username='SimpleUser'), many=True).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)
        client.logout()

    def test_add_in_favorites(self):
        token = Token.objects.get(user__username='SimpleUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(self.url, data={'product_id': 1},
                               headers={'Authorization': 'Token ' + token.key})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_product_in_favorites = Favorites.objects.filter(user__username='SimpleUser').first().product
        self.assertEqual(new_product_in_favorites.name, Product.objects.get(id=1).name)
        client.logout()


# Tests OrderApi

class OrderApiTestCase(APITestCase):
    fixtures = ['db_fixtures.json']
    url = reverse('api:orders-list')

    def test_get_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_authorized(self):
        token = Token.objects.get(user__username='SimpleUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(self.url, headers={'Authorization': 'Token ' + token.key})
        serializer_data = OrderSerializer(Order.objects.filter(initiator__username='SimpleUser'), many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data['results'])
        client.logout()


# Tests ReviewsApi

class ReviewsApiTestCase(APITestCase):
    fixtures = ['db_fixtures.json']
    url = reverse('api:reviews-list')

    def test_get(self):
        response = self.client.get(self.url)
        serializer_data = ReviewsSerializer(Reviews.objects.all(), many=True).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data['results'])

    def test_create(self):
        token = Token.objects.get(user__username='SimpleUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(self.url, data={'rating': 5, 'text': 'new_review', 'product_id': 1},
                               headers={'Authorization': 'Token ' + token.key})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        new_review = Reviews.objects.filter(user__username='SimpleUser').first()
        self.assertEqual(new_review.text, 'new_review')
        client.logout()


# Tests UserApi

class UsersApiTestCase(APITestCase):
    fixtures = ['db_fixtures.json']
    url = reverse('api:users-list')

    def test_get_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_for_simple_user(self):
        token = Token.objects.get(user__username='SimpleUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(self.url, headers={'Authorization': 'Token ' + token.key})
        self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_for_admin_user(self):
        token = Token.objects.get(user__username='AdminUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(self.url, headers={'Authorization': 'Token ' + token.key})
        serializer_data = UserSerializer(User.objects.all(), many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data['results'])
        client.logout()


# Tests RegistrApi

class RegistrApiTestCase(APITestCase):

    def test_create_account(self):
        url = reverse('api:registr')
        response = self.client.post(url,
                                    data={'email': 'test@gmail.com', 'username': 'new_user', 'password': '12345',
                                          'password2': '12345'})
        self.assertEqual({'response': True}, response.data)
        new_user = User.objects.first()
        self.assertEqual(new_user.username, 'new_user')
        self.client.logout()
