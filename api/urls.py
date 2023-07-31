from django.urls import include, path
from rest_framework import routers

from api.views.cart_views import CartModelViewSet
from api.views.category_views import CategoryModelViewSet
from api.views.favorites_views import FavoritesModelViewSet
from api.views.order_views import OrderModelViewSet
from api.views.product_views import ProductModelViewSet
from api.views.registr_views import RegistrUserView
from api.views.reviews_views import ReviewsModelViewSet
from api.views.user_views import UserModelViewSet

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
