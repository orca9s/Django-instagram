from django.shortcuts import render

from ..models import Post


__all__ = (
    'post_list',
)


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    # 포스트 리스트를 보여주는 함수 함수가 호출되면 포스트 리스트 페이지를
    # context에 담아서 불러온다.
    return render(request, 'posts/post_list.html', context)