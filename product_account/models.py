from django.db import models
from django.conf import settings


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField()
    
def __str__(self):
        return self.name