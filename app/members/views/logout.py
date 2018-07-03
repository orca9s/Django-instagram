from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

__all__ = (
    'logout_view',
    'withdraw',
)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        # 로그인 상태에서 로그아웃 클릭시 포스트 리스트로 보내주기
        return redirect('posts:post_list')
    else:
        # get요청으로 접근시 로그인 페이지로 보내주기
        return redirect('members:login')

    # 인증에 성공하면 posts:post-list로 이동
    # 실패하면 다시 memebers:login으로 이동
@login_required
def withdraw(request):
    request.user.delete()
    return redirect('index')