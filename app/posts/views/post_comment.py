from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ..models import Post, Comment

__all__ = (
    'comment_create',
)


@login_required
def comment_create(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)

        Comment.objects.create(
            post=post,
            user=request.user,
            content=request.POST.get('content')
        )

        return redirect('posts:post_detail', post.pk)
    return render(request, 'posts/post_detail.html')
