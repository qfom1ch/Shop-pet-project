from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Reviews


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'image_show', 'text', 'pub_date']
    list_filter = ['product', 'user', 'rating', 'pub_date']
    search_fields = ('name',)
    ordering = ('product',)

    def image_show(self, obj):
        """function to display a picture in the admin panel"""
        if obj.image:
            return mark_safe("<img src='{}' width='130' />".format(obj.image.url))
        return "None"

    image_show.__name__ = "Картинка"
