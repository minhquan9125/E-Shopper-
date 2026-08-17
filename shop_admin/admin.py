from django.contrib import admin
from .models import Country, CustomerUser, Blog


admin.site.register(Country)
admin.site.register(CustomerUser)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ['title', 'author']
    list_filter = ['created_at']

admin.site.register(Blog, BlogAdmin)