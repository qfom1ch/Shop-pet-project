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
    paginate_by = 3
    context_object_name = 'products'
    title = 'Shop - Каталог'

    def get_queryset(self):
        queryset = Product.objects.all().only('name', 'MainImage', 'price', 'short_description', 'slug')
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

    def get_queryset(self):
        queryset = Product.objects.all().only('name', 'MainImage', 'price', 'short_description', 'slug', 'description',
                                              'quantity')
        return queryset

    def get_context_data(self, **kwargs):
        initial = {}
        CHOICES = [(i, i) for i in range(1, self.object.quantity + 1)]

        form = CartAddProductForm(initial=initial)
        form.fields['quantity'] = forms.TypedChoiceField(label='Количество', choices=CHOICES, coerce=int,
                                                         widget=forms.Select(attrs={'class': 'form-control'}))

        context = super().get_context_data(**kwargs)
        context['images'] = ProductImage.objects.filter(product=self.object.id)
        context['cart_product_form'] = form
        context['FavoritesAddProductForm'] = FavoritesAddProductForm()
        context['review_form'] = ReviewForm(initial={'user': self.request.user})
        context['related_products'] = Product.objects.filter(category=self.object.category).exclude(
            id=self.object.id).only(
            'name', 'MainImage', 'price', 'short_description', 'slug')
        return context
