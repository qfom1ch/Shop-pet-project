from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from products.models import ProductCategory
from products.serializers import CategorySerializer


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
