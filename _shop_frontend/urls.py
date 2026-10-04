from django.urls import path,include
from . import views
from cart.views import checkout_view
urlpatterns = [
    path('', views.Home, name='home'),
    path('blog/', include('blog.urls')),
    path("users/", include("users.urls")),
    path('account/', include('product_account.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', checkout_view, name='checkout_view'),

]
