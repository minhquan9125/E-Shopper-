from django.contrib import admin

from django.contrib import admin
from .models import Product,Brand,Category

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','image','price', 'user') 
    search_fields = ('name',)
    list_filter = ('user',)


