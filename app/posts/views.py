from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect

from posts.forms import PostModelForm, PostForm
from posts.models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


# @login_required
# def post_create(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             post = form.post_create(request.user)
#             # form에 들어있는 데이터가 유효한지 검사
#             # is_valid하면 회원가입 버튼을 누른 상태
#             return redirect('posts:post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'posts/post_create.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_list')
    else:
        form = PostModelForm()
    context = {
        'form': form
    }
    return render(request, 'posts/post_create.html', context)

    # PostModelForm을 사용
    #   form = PostModelForm(request.POST,request.FILES)
    #   form.save(author = request.user)


# 데코레이터 안쓰고 delete기능 구현
def delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        if request.user == post.author:
            post.delete()
            return redirect('index')
        else:
            raise PermissionDenied('지울 권환이 없습니다.')
    return HttpResponse('...')

# 데코레이터 안쓰고 delete기능 구현2
# def delete(request, pk):
#     if request.method != 'POST':


# 데코레이터 써서 delete기능 구
# @require_POST
# @login_required()
# def delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if post.author != request.user:
#         raise PermissionDenied('지울 권한이 없습니다.')
#     post.delete()
#     return redirect('posts:post_list')
