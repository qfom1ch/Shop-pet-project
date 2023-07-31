from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from users.models import User
from users.serializers import UserSerializer


class UsersApiTestCase(APITestCase):
    fixtures = ['db_fixtures.json']
    url = reverse('api:users-list')

    def test_get_for_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_for_authorized(self):
        token = Token.objects.get(user__username='SimpleUser')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(self.url, headers={'Authorization': 'Token ' + token.key})
        serializer_data = UserSerializer(User.objects.filter(username='SimpleUser'), many=True).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)
