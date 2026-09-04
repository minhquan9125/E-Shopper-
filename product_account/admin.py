from django.contrib import admin

from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('id', 'name','image','price', 'user') 
    search_fields = ('name',)
    list_filter = ('user',)