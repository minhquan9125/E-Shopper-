from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Blog(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    content = CKEditor5Field("Content", config_name="extends")
    image = models.ImageField(
        upload_to="blog/",
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