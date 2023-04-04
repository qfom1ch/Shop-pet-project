from django.contrib import admin

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
    list_display = ['name', 'slug', 'category', 'price', 'quantity', 'created', 'updated', 'MainImage']
    list_filter = ['quantity', 'created', 'updated', 'category']
    list_editable = ['price', 'quantity', 'category']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImagesInline]
    search_fields = ('name',)
    ordering = ('name',)
