from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect

from config import settings
from members.forms import SignupForm


# User 클래스 자체를 가져올때는 get_user_model()
# Foreignkey에 User모델을 지정할때는 settings.AUTH_USER_MODEL
User = get_user_model()


def login_view(request):
    # 1. POST요청이 왔는데, 요청이 올바르면서 <- 코드에서 어느 위치인지 파악
    # 2. GET parameter에 'next값이 존재할 경우 <-- GET parameter는 requests.GET으로 접근
    # 3. 해당 값(URL)으로 redirect <-redirect() 함수는 URL문자열로도 이동 가능
    # 4. next값이 존재하지 않으면 원래 이동하던 곳으로 그대로 redirect <- 문자열이 있는지 없는지는 if로 판다.

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

            # session_id값을 djagno_sessions테이블에 저장, 데이터는 user와 연결됨
            # 이 함수 실행 후 돌려줄 HTTP Response에는 Set-Cookie헤더를 추가, 내용은 sessionid=<session값>
            login(request, user)
            # 이후 post-list로 redirect

            # 만약에 사용자가 글쓰기 버튼을 통해 로그인을 하였을때 로그인 후 글쓰기 페이지로 보내주기
            # 강사님이 작성한 코드
            next = request.GET.get('next')
            if next:
                return redirect(next)

            # 내가 작성한 코드
            # if request.GET.get('next') == '/posts/create':
            #     return redirect('posts:post_create')
            # 이후 post-list로

            # 글쓰기 버튼 클릭으로 로그인 한게 아니라면 포스트 리스트로 보내주기
            return redirect('posts:post_list')
        else:
            # 로그인 실패시 로그인 페이지로 다시 보내주기
            return redirect('members:login')
    else:
        # get요청으로 들어왔을때 로그인 페이지로 보내주기
        return render(request, 'members/login.html')


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


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        # form에 들어있는 데이터가 유효한지 검사
        if form.is_valid():
            user = form.signup()
            login(request, user)
            return redirect('posts:post_list')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    return render(request, 'members/signup.html', context)


def signup_bak(request):
    context = {
        'errors': [],
    }
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # for문으로 작동하도록 수정
        # locals()

        # 반드시 내용이 채워져야 하는 form의 필드 (위 변수명)
        # hint : requeired_fields를 dict로
        required_fields = ['username', 'email', 'password', 'password2']
        required_fields = {
            # verbose_name은 사용자가 보았을때 알기쉽게 이름을 달아주는 것
            # 단수형= verbose_name, 복수형 = verbose_name_plural
            # verbose_name_plural옵션 대신에 verbose_name에 s 를 붙여줄 수 있다.
            'username': {
                'verbose_name': '아이디',
            },
            'email': {
                'verbose_name': '이메일',
            },
            'password': {
                'verbose_name': '비밀번호',
            },
            'password2': {
                'verbose_name': '비밀번호 확인',
            },
        }
        for field_name in required_fields.keys():
            # print('field_name:', field_name)
            # print('locals()[field_name]:', locals()[field_name])
            if not locals()[field_name]:
                context['errors'].append('{}을(를) 채워주세요'.format(
                    required_fields[field_name]['verbose_name']
                ))
        # print(locals())
        # if not username:
        #     context['errors'].append('username을 채워주세요')
        # if not email:
        #     context['errors'].append('email을 채워주세요')
        # if not password:
        #     context['errors'].append('password를 채워주세요')
        # if not password2:
        #     context['errors'].append('password check를 채워주세요')

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
            context['errors'].append('이미 사용중인 아이디 입니다.')
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
            return render(request, 'members/signup_bak.html', context)
    return render(request, 'members/signup_bak.html')


@login_required
def withdraw(request):
    request.user.delete()
    return redirect('index')


def follow_toggle(request):
    """
    GET요청은 처리하지 않음

    POST요청일 때
        1.request.POST로 'user_pk'값을 전달받음
          pk가 user_pk인 User를 user에 할당
        2.request.user의
    """
    pass


def facebook_login(request):
    # GET parameter의 'code'에 값이 전달됨 (authentication code)
    # 전달받은 인증코드를 사용해서
    code = request.GET.get('code')
    # 왼쪽 액세스 코드 교환 엔드포인트에 Http GET요청 후,
    # 결과 response.text값을 HttpResponse에 출력
    url = 'https://graph.facebook.com/v3.0/oauth/access_token?'
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        'client_secret': settings.FACEBOOK_APP_SECRET_CODE,
        'code': code,
    }
    response = requests.get(url, params)
    # 파이선에 내장된json모듈을 사용해서, JSON형식의 텍스트를 파이썬 Object로 변경
    response_dict = json.loads(response.text)

    # 위와 같은 결과
    response_dict = response.json()

    # access_token값만 꺼내서 HttpResponse로 출력
    # return HttpResponse(response_dict['access_token'])

    access_token = response_dict['access_token']

    # debug_token에 요청 보내고 결과 받기
    # 받은 결과의 'data'값을 HttpResponse로 출력
    #   input_token은 위의 'access_token'
    #   access_token은 {client_id}|{client_secret}값
    url = 'https://graph.facebook.com/debug_token?'
    params = {
        "input_token": access_token,
        "access_token": '{}|{}'.format(
            settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_APP_SECRET_CODE
        )
    }
    response = requests.get(url, params)

    # GraphAPI를 통해서 'me'(user)를 이용해서 Facebook User정보 받아오기
    url = 'https://graph.facebook.com/v3.0/me'
    params = {
        'fields': ','.join([
            'id',
            'name',
            'first_name',
            'last_name',
            'picture'
        ]),
        'access_token': access_token,
    }
    response = requests.get(url, params)
    response_dict = response.json()

    # 받아온 정보 중 회원가입에 필요한 요소들 꺼내기
    facebook_user_id = response_dict['id']
    first_name = response_dict['first_name']
    last_name = response_dict['last_name']
    url_img_profile = response_dict['picture']['data']['url']

    # facebook_user_id가 username인 User를 기준으로 가져오거나 새로생성
    user, user_created = User.objects.get_or_create(
        username=facebook_user_id,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
        },
    )
    # 유저가 새로 생성되었다면
    # if user_created:
    #     user.first_name = first_name
    #     user.last_name = last_name
    #     user.save()
    # 생성한 유저로 로그인
    login(request, user)

    return redirect('index')


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
