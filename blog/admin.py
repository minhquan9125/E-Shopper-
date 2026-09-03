from django.contrib import admin
from .models import  Blog ,Rate,Comment

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ['title', 'author']
    list_filter = ['created_at']

admin.site.register(Blog, BlogAdmin) 
class RateAdmin(admin.ModelAdmin):
    list_display = ('id_rate', 'id_blog', 'id_user', 'rate', 'created_at')
    list_filter = ('rate', 'created_at')
admin.site.register(Rate, RateAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('cmt','id_user','id_blog','name_user','level','created_at')
    search_fields  = ('id_user','id_blog')
    list_filter = ['created_at']
admin.site.register(Comment,CommentAdmin)