from django.views.generic.list import ListView

from common.views import TitleMixin

from .models import Product, ProductCategory


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    context_object_name = 'products'
    title = 'Shop - Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['category_id'] = self.kwargs.get('category_id')  # <-------------------------------
        return context
