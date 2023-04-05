from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from common.views import TitleMixin
from .forms import SortForm
from .models import Product, ProductCategory, ProductImage


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    context_object_name = 'products'
    title = 'Shop - Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()

        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category_id = ProductCategory.objects.get(slug=category_slug).id
            queryset = queryset.filter(category_id=category_id)

        sort_form = SortForm(self.request.GET)
        if sort_form.is_valid():
            needed_sort = sort_form.cleaned_data.get("sort_form")
            if needed_sort == 'price':
                queryset = queryset.order_by("price")
            if needed_sort == '-price':
                queryset = queryset.order_by("-price")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = ProductCategory.objects.all()
        context['form'] = SortForm()

        sort = self.request.GET.get('sort_form', None)
        context['sort'] = sort

        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = ProductCategory.objects.get(slug=category_slug)
        context['category_slug'] = category_slug

        return context


class ProductsSingleView(TitleMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    title = 'Shop - Информация о продукте'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ProductImage.objects.filter(product=self.object.id)
        return context
