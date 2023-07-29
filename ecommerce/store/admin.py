from django.contrib import admin
from .models import Category, Product
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =['name', 'slug', 'price', 'available']
    # list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']

    