from django.shortcuts import render

from ..models import Post

__all__ = (
    'post_detail',
)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post,
    }
    # 포스트 디테일을 보여주는 함수이다. urls에서 호출을 하면
    # context에 내용을 담아서 보내준다.
    return render(request, 'posts/post_detail.html', context)
