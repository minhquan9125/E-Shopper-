from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
class Country(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self) : 
        return self.name

class CustomerUser(AbstractUser):
    avatar=models.ImageField(upload_to='avatars/', null = True , blank=True)
    id_country=models.ForeignKey(Country, on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.username