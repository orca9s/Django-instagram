from django.shortcuts import render

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


def post_create(request):
    context = {
        'posts': posts,
    }
    # 새 포트스를 만들기
    # 만든 후에는 해당하는 post_detail로 이동
    # forms.py에 PostForm을 구현해서 사용

    # bound form (include file)
    # PostForm(request.POST)
    # PostForm(request.POST, request.FILES)

    # POST method에서는 생성후 redirect
    # GET method에서는 form이 보이는 템플릿 렌더링
    return render(request, 'posts/post_create.html', context)
