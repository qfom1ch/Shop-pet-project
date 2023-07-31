from django import forms
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from cart.forms import CartAddProductForm, CartAddProductFormWithoutChoice
from common.views import TitleMixin
from favorites.forms import FavoritesAddProductForm
from reviews.forms import ReviewForm

from .forms import SortForm
from .models import Product, ProductCategory, ProductImage


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 7
    context_object_name = 'products'
    title = 'Shop - Каталог'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = Product.objects.select_related('category') \
                .filter(category__slug=category_slug) \
                .only('name', 'MainImage', 'price', 'short_description', 'slug', 'category__slug')
        else:
            queryset = Product.objects.all().only('name', 'MainImage', 'price', 'short_description', 'slug')

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
    queryset = Product.objects.all().only('name', 'MainImage', 'price', 'short_description', 'slug', 'description',
                                          'quantity')
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    title = 'Shop - Информация о продукте'

    def get_context_data(self, **kwargs):
        initial = {}
        choices = [(i, i) for i in range(1, self.object.quantity + 1)]
        cart_add_form = CartAddProductForm(initial=initial)
        cart_add_form.fields['quantity'] = forms.TypedChoiceField(label='Количество', choices=choices, coerce=int,
                                                                  widget=forms.Select(attrs={'class': 'form-control'}))

        context = super().get_context_data(**kwargs)
        context['images'] = ProductImage.objects.filter(product=self.object.id)
        context['cart_product_form'] = cart_add_form
        context['FavoritesAddProductForm'] = FavoritesAddProductForm()
        context['review_form'] = ReviewForm(initial={'user': self.request.user})
        category = Product.objects.select_related('category').filter(id=self.object.id) \
            .values_list('category__id', flat=True)[0]
        context['related_products'] = Product.objects.filter(category=category).exclude(
            id=self.object.id).only(
            'name', 'MainImage', 'price', 'short_description', 'slug')
        return context
