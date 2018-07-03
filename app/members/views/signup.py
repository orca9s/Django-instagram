from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect, render

from members.forms import SignupForm

User = get_user_model()

__all__ = (
    'signup',
)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        # form에 들어있는 데이터가 유효한지 검사
        if form.is_valid():
            user = form.signup()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
