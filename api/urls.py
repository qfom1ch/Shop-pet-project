from django.urls import include, path
from rest_framework import routers

from api.views import (CartModelViewSet, CategoryModelViewSet,
                       FavoritesModelViewSet, OrderModelViewSet,
                       ProductModelViewSet, RegistrUserView,
                       ReviewsModelViewSet, UserModelViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'category', CategoryModelViewSet, basename='category')
router.register(r'products', ProductModelViewSet, basename='products')
router.register(r'cart', CartModelViewSet, basename='cart')
router.register(r'favorites', FavoritesModelViewSet, basename='favorites')
router.register(r'orders', OrderModelViewSet, basename='orders')
router.register(r'reviews', ReviewsModelViewSet, basename='reviews')
router.register(r'users', UserModelViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('registr/', RegistrUserView.as_view(), name='registr')
]
