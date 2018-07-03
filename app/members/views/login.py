from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

__all__ = (
    'login_view',
)


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