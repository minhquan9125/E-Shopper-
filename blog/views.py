from django.shortcuts import render

def Blog(request):
    return render(request, 'blog.html')  