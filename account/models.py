from django.db import models
from django.conf import settings


class Product(models.Model):
    name = models.TextField(max_length=20)
    image=models.ImageField(upload_to='')


    
