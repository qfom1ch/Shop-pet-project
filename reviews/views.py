from django.shortcuts import redirect
from django.views.generic.base import View

from products.models import Product
from reviews.models import Reviews

from .forms import ReviewForm


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST, request.FILES)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.FILES:
                form.image = request.FILES['image']
            form.product = product
            form.save()
        return redirect(request.META['HTTP_REFERER'])


class DeleteReview(View):
    """Отзывы"""

    def get(self, request, pk):
        Reviews.objects.get(id=pk).delete()
        return redirect(request.META['HTTP_REFERER'])
