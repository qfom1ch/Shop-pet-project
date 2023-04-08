from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django import forms
from common.views import TitleMixin
from .forms import SortForm
from .models import Product, ProductCategory, ProductImage

from cart.forms import CartAddProductForm, CartAddProductFormWithoutChoice
from favorites.forms import FavoritesAddProductForm

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
        context['cart_product_form_without_choice'] = CartAddProductFormWithoutChoice()
        context['FavoritesAddProductForm'] = FavoritesAddProductForm()
        return context


class ProductsSingleView(TitleMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    title = 'Shop - Информация о продукте'

    def get_context_data(self, **kwargs):
        product = Product.objects.get(id = self.object.id)
        initial = {}
        CHOICES = [(i, i) for i in range(1, product.quantity+1)]

        form = CartAddProductForm(initial=initial)
        form.fields['quantity'] = forms.TypedChoiceField(label='Количество',  choices=CHOICES, coerce=int,
                                      widget=forms.Select(attrs={'class': 'form-control'}))

        context = super().get_context_data(**kwargs)
        context['images'] = ProductImage.objects.filter(product=self.object.id)
        context['cart_product_form'] = form
        context['FavoritesAddProductForm'] = FavoritesAddProductForm()
        return context


# def product_detail(request, id, slug):
#     product = get_object_or_404(Product,
#                                 id=id,
#                                 slug=slug,
#                                 available=True)
#     cart_product_form = CartAddProductForm()
#     return render(request, 'shop/product/detail.html', {'product': product,
#                                                         'cart_product_form': cart_product_form})