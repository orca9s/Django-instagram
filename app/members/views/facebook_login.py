from django.contrib.auth import login, get_user_model, authenticate

from django.shortcuts import redirect


__all__ = (
    'facebook_login',
)

User = get_user_model()


def facebook_login(request):
    code = request.GET.get('code')
    user = authenticate(request, code=code)
    if user is not None:
        login(request, user)
        return redirect('index')
    return redirect('members:login')
    # 유저가 새로 생성되었다면
    # if user_created:
    #     user.first_name = first_name
    #     user.last_name = last_name
    #     user.save()
    # 생성한 유저로 로그인
