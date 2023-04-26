from rest_framework import serializers
from favorites.models import Favorites
from products.serializers import ProductSerializer


class FavoritesSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Favorites
        fields = ('id', 'product')

