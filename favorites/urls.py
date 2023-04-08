from django.urls import path

from .views import favorites, favorites_add, favorites_remove

app_name = 'favorites'

urlpatterns = [
    path('', favorites, name='favorites'),
    path('favorites_add/<int:product_id>/', favorites_add, name='favorites_add'),
    path('favorites_remove/<int:product_id>/', favorites_remove, name='favorites_remove'),
]