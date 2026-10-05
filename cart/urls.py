from django.urls import path

from . import views


urlpatterns = [
    path('', views.view_product_cart, name='cart_view'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:id>/', views.update_cart_view, name='update_cart_view'),
    path('delete/<int:id>/', views.delete_product_cart_view, name='delete_product_cart_view'),
    path('checkout/', views.checkout_view, name='checkout_view'),
]
