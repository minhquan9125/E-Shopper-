from django.shortcuts import render
from .models import Blog
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

def blog_list_view(request):
    blog_list = Blog.objects.all().order_by('created_at')
    pagnitor = Paginator(blog_list, 3)
    page_number = request.GET.get('page')
    page_obj = pagnitor.get_page(page_number)
    return render(request, 'blog.html', {
        'page_obj': page_obj,
        'pagnitor': pagnitor
    })
def blog_detail_view(request, id):
    blog = Blog.objects.get(id=id)
    return render(request, 'blog-detail.html', {'blog': blog})