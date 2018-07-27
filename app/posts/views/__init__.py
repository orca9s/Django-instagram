from . post_create import *
from . post_detail import *
from . post_list import *
from . post_delete import *
from . post_comment import *


# from django.contrib.auth import authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.views import login
# from django.core.exceptions import PermissionDenied
# from django.http import HttpResponse
# from django.shortcuts import render, redirect
#
# from posts.forms import PostForm, PostModelForm
# from posts.models import Post, Comment
#
#
# def post_list(request):
#     posts = Post.objects.all()
#     context = {
#         'posts': posts,
#     }
#     # 포스트 리스트를 보여주는 함수 함수가 호출되면 포스트 리스트 페이지를
#     # context에 담아서 불러온다.
#     return render(request, 'posts/post_list.html', context)
#
#
# def post_detail(request, pk):
#     post = Post.objects.get(pk=pk)
#     context = {
#         'post': post,
#     }
#     # 포스트 디테일을 보여주는 함수이다. urls에서 호출을 하면
#     # context에 내용을 담아서 보내준다.
#     return render(request, 'posts/post_detail.html', context)
#
#
# # @login_required
# # def post_create(request):
# #     if request.method == 'POST':
# #         form = PostForm(request.POST, request.FILES)
# #
# #         if form.is_valid():
# #             post = form.post_create(request.user)
# #             # form에 들어있는 데이터가 유효한지 검사
# #             # is_valid하면 회원가입 버튼을 누른 상태
# #             return redirect('posts:post_detail', pk=post.pk)
# #     else:
# #         form = PostForm()
# #     context = {
# #         'form': form,
# #     }
# #     return render(request, 'posts/post_create.html', context)
#
# # login_required는 로그인이 되어있을 때만 실행을 하게 한다.
# @login_required
# def post_create(request):
#     # 포스트 요청으로 들어올경우
#     if request.method == 'POST':
#         form = PostModelForm(request.POST, request.FILES)
#         # form에 들어있는 데이터가 유효한지 검사
#         # 유효성 검사 무엇을위한?
#         # 유효성 검사는 form에서 지정한 필드를 충족하는지 검사
#         if form.is_valid():
#             post = form.save(commit=False)
#             # post.author에다가 현재 로그인중인 user를 할당
#             post.author = request.user
#             # 포스트를 저장
#             post.save()
#             # 글작성 완료후 디테일 페이지로 리턴
#             return redirect('posts:post_detail', pk=post.pk)
#     else:
#         # 이 form에는 도대체 무엇을 담는것인가?
#         form = PostModelForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'posts/post_create.html', context)
#
#     # PostModelForm을 사용
#     #   form = PostModelForm(request.POST,request.FILES)
#     #   form.save(author = request.user)
#
#
# # 데코레이터 안쓰고 delete기능 구현
# def delete(request, pk):
#     if request.method == 'POST':
#         post = Post.objects.get(pk=pk)
#         if request.user == post.author:
#             post.delete()
#             return redirect('index')
#         else:
#             raise PermissionDenied('지울 권한이 없습니다.')
#     return HttpResponse('...')
#
#
# @login_required
# def comment_create(request, pk):
#     if request.method == 'POST':
#         post = Post.objects.get(pk=pk)
#
#         Comment.objects.create(
#             post=post,
#             user=request.user,
#             content=request.POST.get('content')
#         )
#
#         return redirect('posts:post_detail', post.pk)
#     return render(request, 'posts/post_detail.html')
# # 데코레이터 안쓰고 delete기능 구현2
# # def delete(request, pk):
# #     if request.method != 'POST':
#
#
# # 데코레이터 써서 delete기능 구
# # @require_POST
# # @login_required()
# # def delete(request, pk):
# #     post = get_object_or_404(Post, pk=pk)
# #     if post.author != request.user:
# #         raise PermissionDenied('지울 권한이 없습니다.')
# #     post.delete()
# #     return redirect('posts:post_list')
