from django.contrib.auth import authenticate
from django.contrib.auth.views import login
from django.shortcuts import render, redirect


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

    # 인증에 성공하면 posts:post-list로 이동
    # 실패하면 다시 memebers:login으로 이동
