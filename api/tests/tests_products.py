from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from products.models import Product
from products.serializers import ProductSerializer


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
