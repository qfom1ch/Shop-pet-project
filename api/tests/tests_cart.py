from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from cart.models import Cart
from cart.serializers import CartSerializer
from products.models import Product


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
