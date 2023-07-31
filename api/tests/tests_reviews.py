from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from reviews.models import Reviews
from reviews.serializers import ReviewsSerializer


class ReviewsApiTestCase(APITestCase):
    fixtures = ['db_fixtures.json']
    url = reverse('api:reviews-list')

    # don't pass tests with select_related in views
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
