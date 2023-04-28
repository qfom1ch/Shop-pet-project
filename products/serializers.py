from rest_framework import serializers

from products.models import Product, ProductCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=ProductCategory.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'short_description', 'price', 'quantity', 'category')  # 'MainImage'
