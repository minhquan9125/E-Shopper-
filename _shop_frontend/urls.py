from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.Home, name='home'),
    path('blog/', include('blog.urls')),
    path("users/", include("users.urls")),

]