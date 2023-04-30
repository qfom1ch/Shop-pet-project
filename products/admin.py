from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, ProductCategory, ProductImage


@admin.register(ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductImagesInline(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'quantity', 'image_show', 'created', 'updated']
    list_filter = ['quantity', 'created', 'updated', 'category']
    list_editable = ['price', 'quantity', 'category']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImagesInline]
    search_fields = ('name',)
    ordering = ('name',)

    def image_show(self, obj):
        """function to display a picture in the admin panel"""
        if obj.MainImage:
            return mark_safe("<img src='{}' width='130' />".format(obj.MainImage.url))
        return "None"

    image_show.__name__ = "Картинка"
