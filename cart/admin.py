from django.contrib import admin

from .models import History


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'id_user', 'price')
    search_fields = ('name', 'email', 'phone', 'id_user__username')
    list_filter = ('id_user',)
