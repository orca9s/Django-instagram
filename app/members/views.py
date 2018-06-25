from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.views import login, logout
# from django.http import HttpResponse
from django.shortcuts import render, redirect


# User 클래스 자체를 가져올때는 get_user_model()
# Foreignkey에 User모델을 지정할때는 settings.AUTH_USER_MODEL
User = get_user_model()


def login_view(request):
    # 1. member.urls <-'members/'로 include 되도록 config.urls모듈에 추가
    # 2. path구현 (URL: '/membsers/login/')
    # 3. path와 이 view 연결
    # 4. 일단 잘 나오는지 확인
    # 5. 잘 나오면 form을 작성 (username, password를 받는 input2개)
    # 6. form작성후에는 POST방식 요청을 보내서 이 뷰에서 request.POST에 요청이 잘 왔는지 확인
    # 7. 일단은 받은 username, password값을 HttpResponse에 보여주도록 한다.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # 받은 username과 password에 해당하는 User가 있는지 인증
        user = authenticate(request, username=username, password=password)

        # 인증에 성공한 경우
        if user is not None:
            # 세션값을 만들어 DB에 저장하고, HTTP response의 Cookie에 해당값을 담아보내도록 하는
            # login()함수를 실행한다
            login(request, user)
            # 이후 post-list로
            return redirect('posts:post_list')
        else:
            return redirect('members:login')
    else:
        return render(request, 'members/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post_list')
    else:
        return redirect('members:login')

    # 인증에 성공하면 posts:post-list로 이동
    # 실패하면 다시 memebers:login으로 이동


def signup_view(request):
    context = {
        'errors': [],
    }
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # 입력 데이터 채워넣기
        context['username'] = username
        context['email'] = email

        # form 에서 전송된 데이터들이 올바른지 검사
        if User.objects.filter(username=username).exists():
            # 단순 redirect가 아니라, render를 사용
            # render에 context를 전달
            #   'errors'키에 List를 할당하고, 해당 리스트에
            #   '유저가 이미 존재함' 문자열을 추가해서 전달
            #   템플릿에서든 전달받은 errors를 순회하며 에러메시지를 출력
            context['errors'].append('유저가 이미 존재함')
        if password != password2:
            context['errors'].append('패스워드가 일치 하지 않음')

        # errors가 존재하면 render
        if not context['errors']:
            # errors가 없으면 유저 생성 루틴 실행
            User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            return redirect('posts:post_list')
        else:
            return render(request, 'members/signup.html', context)


# def signup(request):
#     if request.method == 'POST':
#         # exists를 사용해서 유저가 이미 존재하면 signup으로 다시 redirect
#         # 존재하지 않는 경우에만 아래 로직 실
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = User.objects.create_user(
#             username=username,
#             password=password,
#         )
#         print(request.user.is_autenticated)
#         login(request, user)
#         return redirect('index')
#     return render(request, 'members/signup.html')
