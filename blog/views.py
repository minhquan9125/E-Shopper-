from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Avg

from .models import Blog, Rate,Comment


def blog_list_view(request):
    blog_list = Blog.objects.all().order_by('created_at')
    paginator = Paginator(blog_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog.html',
        {'page_obj': page_obj, 'paginator': paginator},
    )


def blog_detail_view(request, id):
    blog = get_object_or_404(Blog, id=id)
    avg_rate = round(Rate.objects.filter(id_blog=id).aggregate(avg=Avg('rate'))['avg'] or 0, 1)
    comments = Comment.objects.filter(id_blog=id).order_by('-created_at')
    return render(request, 'blog-detail.html', {
        'blog': blog,
        'avg_rate':avg_rate,
        'comments': comments

        })


def rate_blog_view(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse(
                {'success': False, 'error': 'Vui lòng đăng nhập để đánh giá!'}
            )
        id_blog = request.POST.get('id_blog')
        rate = request.POST.get('rate')

        try:    
            blog = Blog.objects.get(id=id_blog)
            Rate.objects.create(id_blog=blog, rate=int(rate), id_user=request.user)
            return JsonResponse({'success': True})
        except Blog.DoesNotExist:
            return JsonResponse(
                {'success': False, 'error': 'Bài viết không tồn tại'}
            )
        except Exception as e:
            return JsonResponse({'success': False, 'error': "Bạn đã đánh giá bài viết này rồi"})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def blog_comment_view(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request'})

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Vui lòng đăng nhập để bình luận!'})

    blog_id = request.POST.get('blog_id')
    comment_text = request.POST.get('comment') or request.POST.get('cmt')
    level = int(request.POST.get('level', 0))
    parent_id = request.POST.get('parent_id')

    try:
        blog = Blog.objects.get(id=blog_id)
        parent = None
        if level == 1 and parent_id:
            parent = Comment.objects.get(id=parent_id, id_blog=blog)

        comment = Comment.objects.create(
            cmt=comment_text,
            id_blog=blog,
            id_user=request.user,
            name_user=request.user.username,
            level=level,
            parent=parent
        )

        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'comment': comment.cmt,
            'user_name': comment.name_user,
            'avatar': request.user.avatar.url if request.user.avatar else '',
            'level': comment.level,
            'parent_id': comment.parent_id,
        })

    except Blog.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Blog not found'})
    except Comment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Comment cha không tồn tại'})

        