import json

from django.db import models
from django.conf import settings


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=50)
    price = models.FloatField()
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    id_brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    status = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)
    image = models.JSONField(default=list, blank=True)
    company = models.CharField(max_length=50, default='', blank=True)
    detail = models.TextField(default='', blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    