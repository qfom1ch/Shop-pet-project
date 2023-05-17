from .models import ProductCategory


def categories(request):
    """Returns all categories."""
    return {'categories': ProductCategory.objects.all().only}
