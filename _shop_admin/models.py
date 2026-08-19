from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from ckeditor_uploader.fields import RichTextUploadingField # CKEditor
class Country(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self) : 
        return self.name

class CustomerUser(AbstractUser):
    avatar=models.ImageField(upload_to='avatars/', null = True , blank=True)
    id_country=models.ForeignKey(Country, on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.username


class Blog(models.Model):
    title = models.CharField(max_length=50)
    description=models.TextField(max_length=100)
    content=RichTextUploadingField()
    image=models.ImageField(upload_to='shop_admin/image/', null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

