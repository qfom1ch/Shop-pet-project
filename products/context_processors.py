from .models import ProductCategory, Product


def categories(request):
    """Returns all categories."""
    return {'categories': ProductCategory.objects.all()}
