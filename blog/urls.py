
from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.blog_list_view, name='blog_list_view'),
    path('blog/<int:id>/', views.blog_detail_view, name='blog_detail_view'),
    path('rate/', views.rate_blog_view, name='rate_blog_view'),
    path('comment/', views.blog_comment_view, name='blog_comment_view'),
    ]   