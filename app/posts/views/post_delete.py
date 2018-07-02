from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect

from posts.models import Post


__all__ = (
    'delete',
)


def delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        if request.user == post.author:
            post.delete()
            return redirect('index')
        else:
            raise PermissionDenied('지울 권한이 없습니다.')
    return HttpResponse('...')

