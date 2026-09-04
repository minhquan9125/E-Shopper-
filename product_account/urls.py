
from django.urls import path
from . import views

urlpatterns = [
    path('update/', views.update_user_view, name='update_user_view'),
    path('product/', views.product_view, name='product_view'),

    ]   