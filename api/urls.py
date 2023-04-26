from django.urls import include, path
from rest_framework import routers

from api.views import CategoryModelViewSet, ProductModelViewSet, CartModelViewSet, FavoritesModelViewSet, \
    OrderModelViewSet, ReviewsModelViewSet, UserModelViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'category', CategoryModelViewSet)
router.register(r'products', ProductModelViewSet)
router.register(r'cart', CartModelViewSet)
router.register(r'favorites', FavoritesModelViewSet)
router.register(r'orders', OrderModelViewSet)
router.register(r'reviews', ReviewsModelViewSet)
router.register(r'users', UserModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
