from django.urls import path

from .views import ProductsListView, ProductsSingleView

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='products'),
    path('category/<slug:category_slug>/', ProductsListView.as_view(), name='category'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('product_detail/<slug:slug>/', ProductsSingleView.as_view(), name='product_detail'),
]
