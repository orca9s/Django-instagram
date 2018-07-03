# 1. settings.py에 AUTHENTICATION_BACKENDS항목을 작성
#    Django가 기본적으로 지원하는 Default값 (ModelBackend)를
#    포함한 리스트를 작성 (FacebookBackend로의 문자열)
# 2. facebook_login view를 수정
#    user를 받아오는 과정에
#    user = authenticate(request, code=code)를 사용
import json

from django.contrib.auth import get_user_model
import requests
from config import settings

User = get_user_model()
class FacebookBackend:
    def authenticate(self, request, code):
        '''
        Facebooke의 Authorization Code가 주어졌을 때
        적절히 처리해서
        facebook의 user_id에 해당하는 User가 있으면 해당 User를 리턴
        없으면 생성해서 리턴
        :param request: View의 HttpRequest object
        :param code: Facebook Authorization code
        :return: User인스턴스
        '''

        def get_access_token(code):
            """
            Authorization code를 사용해 엑세스 토큰을 받아옴
            :param code: 유저의 페이스북 인증 후 전달되는 Authorization code
            :return: 엑세스 토큰 문자열
            """
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
            return access_token

        def debug_token(token):
            '''
            주어진 token을 Facebook의 debug_token API Endpoint를 사용해 검사
            :param token: 엑세스 토큰
            :return: JSON응답을 파싱한 Object
            '''

            # debug_token에 요청 보내고 결과 받기
            # 받은 결과의 'data'값을 HttpResponse로 출력
            #   input_token은 위의 'access_token'
            #   access_token은 {client_id}|{client_secret}값
            # debug_token은 토큰이 유효한지 검사하고 사용자의 토큰이 맞는지 검사하는 일을 한다.
            url = 'https://graph.facebook.com/debug_token?'
            params = {
                "input_token": token,
                "access_token": '{}|{}'.format(
                    settings.FACEBOOK_APP_ID,
                    settings.FACEBOOK_APP_SECRET_CODE
                )
            }
            response = requests.get(url, params)
            return response.json()

        # get_user_info('<token value>') <- 기존의 5가지 값을 fields로
        # get_user_info('<token value>', ['id', 'name', 'first_name'])<- 주어진 3개

        def get_user_info(token, fields=('id', 'name', 'first_name', 'last_name', 'picture')):
            # 동적으로 params의 'fields'값을 채울 수 있도록 매개변수 및 함수 내 동작 변경
            '''
            주어진 token에 해당하는 Facebook User의 정보를 리턴
            'id', 'name', 'first_name', 'last_name', 'picture'
            :param token: Facebook User토큰
            :return:
            '''
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
                'access_token': token,
            }
            response = requests.get(url, params)
            return response.json()

        def create_user_from_facebook_user_info(user_info):
            '''
            Facebook GraphAPI의 'User'에 해당하는 응답인 user_info로부터
            id, first_name, last_name, picture항목을 사용해서
            Django의 User를 가져오거나 없는경우 새로 만듬 (get_or_create)
            :param user_info:Facebook GraphAPI - User의 응답
            :return: get_or_create의 결과 tuple (User instance, Bool(created))
            '''

            # 받아온 정보 중 회원가입에 필요한 요소들 꺼내기
            facebook_user_id = user_info['id']
            first_name = user_info['first_name']
            last_name = user_info['last_name']
            url_img_profile = user_info['picture']['data']['url']

            # facebook_user_id가 username인 User를 기준으로 가져오거나 새로생성
            return User.objects.get_or_create(
                username=facebook_user_id,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                },
            )

        access_token = get_access_token(code)
        user_info = get_user_info(access_token)
        user, user_created = create_user_from_facebook_user_info(user_info)
        return user

    def get_user(self, user_id):
        '''
        user_id(primary_key값)이 주어졌을 때
        해당 User가 존재하면 반환하고, 없으면 None을 반환한다.
        :param user_id: User모델의 primary_key값
        :return: primary_key에 해당하는 User가 존재하면 User인스턴스, 아니면 None
        '''
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise
