from django.shortcuts import render

from posts.models import Post


def post_list(request):
    return render(request, 'posts/post_list.html')


def post_detail(request, pk):
    return render(request, 'posts/post_detail.html')
