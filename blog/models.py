from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from users.models import CustomerUser

class Blog(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    content = CKEditor5Field("Content", config_name="extends")
    image = models.ImageField(
        upload_to="static/blog/",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.title
class Rate(models.Model):
    id_rate = models.AutoField(primary_key=True)
    id_blog = models.ForeignKey(Blog,on_delete=models.CASCADE) 
    id_user =  models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('id_blog', 'id_user')

class Comment(models.Model):
    cmt = models.CharField(max_length=50)
    id_user =  models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    id_blog = models.ForeignKey(Blog,on_delete=models.CASCADE) 
    avatar=models.ImageField(upload_to='avatars/', null = True , blank=True)
    name_user = models.CharField(max_length=100)   
    level= models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'
    def __str__(self):
        return f'{self.name_user}: {self.cmt}'

