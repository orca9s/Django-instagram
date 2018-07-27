from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from ..models import Post


__all__ = (
    'post_like',
)


@login_required
@require_POST
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    request.user.like_posts.add(post)
    return redirect('posts:post_detail', pk=pk)
