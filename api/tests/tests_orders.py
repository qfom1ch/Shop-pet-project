from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from orders.models import Order
from orders.serializers import OrderSerializer


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
