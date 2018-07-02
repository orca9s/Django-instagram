from django.urls import path

from .views import login_view, logout_view, signup, withdraw, facebook_login

app_name = 'members'
urlpatterns = [
    # 로그인 버튼 클릭시 실행
    path('login/', login_view, name='login'),
    # 로그아웃 버튼 클릭시 실행
    path('logout/', logout_view, name='logout'),
    # 회원가입 버튼 클릭시 실행
    path('signup/', signup, name='signup'),
    # 회원탈퇴 버튼 클릭시 실행
    path('withdraw/', withdraw, name='withdraw'),
    # 페이스북 로그인
    path('facebook-login/', facebook_login, name='facebook_login')
]
