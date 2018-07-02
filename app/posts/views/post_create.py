from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from posts.forms import PostModelForm

__all__ = (
    'post_create',
)


@login_required
def post_create(request):
    # 포스트 요청으로 들어올경우
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        # form에 들어있는 데이터가 유효한지 검사
        # 유효성 검사 무엇을위한?
        # 유효성 검사는 form에서 지정한 필드를 충족하는지 검사
        if form.is_valid():
            post = form.save(commit=False)
            # post.author에다가 현재 로그인중인 user를 할당
            post.author = request.user
            # 포스트를 저장
            post.save()
            # 글작성 완료후 디테일 페이지로 리턴
            return redirect('posts:post_detail', pk=post.pk)
    else:
        # 이 form에는 도대체 무엇을 담는것인가?
        form = PostModelForm()
    context = {
        'form': form
    }
    return render(request, 'posts/post_create.html', context)