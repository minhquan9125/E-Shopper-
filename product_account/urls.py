
from django.urls import path
from . import views

urlpatterns = [
    path('update/', views.update_user_view, name='update_user_view'),
    path('product/', views.product_view, name='product_view'),
    path('my-product/', views.my_product_view, name='my_product_view'),
    path('my-product/', views.my_product_view, name='my_product_view'),
    path('edit-product/<int:id>/', views.edit_roduct_view, name='edit_roduct_view'),
    path('delete-product/<int:id>/', views.delete_product_view, name='delete_product_view'),
    path('product-detail/<int:id>/',views.product_detail_view,name='product_detail_view'),


]
