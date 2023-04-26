from rest_framework import serializers

from products.serializers import ProductSerializer
from reviews.models import Reviews
from users.serializers import UserSerializer


class ReviewsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    user = UserSerializer()

    class Meta:
        model = Reviews
        fields = ('id', 'product', 'user', 'text', 'image', 'pub_date', 'rating')
        read_only_fields = ('pub_date',)
