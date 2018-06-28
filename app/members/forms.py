from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class SignupForm(forms.Form):
    CHOICES_GENDER = {
        ('m', '남성'),
        ('f', '여성'),
        ('x', '선택안함'),
    }
    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    email = forms.EmailField(
        label='이메일',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    site = forms.CharField(
        label='사이트 주소',
        required=False,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    introduce = forms.CharField(
        label='소개하기',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    gender = forms.ChoiceField(
        label='성별',
        required=False,
        choices=CHOICES_GENDER,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )
    img_profile = forms.ImageField(
        label='프로필 사진',
        required=False,
    )

    def clean_username(self):

        username = self.cleaned_data['username']
        # username field의 clean()실행 결과rk self.cleaned_data['username']에 있음
        # exists() 입력받은 값이 이미 있는지 중복 검사 키와 벨류 모두 받아옴
        if User.objects.filter(username=username).exists():
            raise ValidationError('이미 사용중인 아이디 입니다.')
        return username

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            self.add_error('password2', '비밀번호가 비밀번호 확인과 일치하지 않습니다.')
        return self.cleaned_data

    def signup(self):
        fields = [
            'username',
            'email',
            'password',
            'gender',
            'img_profile',
            'introduce',
            'site',
        ]
        create_user_dict = {}
        for key, value in self.cleaned_data.items():
            if key in fields:
                create_user_dict[key] = value
                print('success')

        # dict comprehesion으로
        create_user_dict = {key: value for key, value in self.cleaned_data.items() if key in fields}

        # filter를 사용
        def in_fields(item):
            return item[0] in fields

        result = filter(in_fields, self.cleaned_data.items())
        for item in result:
            create_user_dict[item[0]] = item[1]

        # filter결과를 dict함수로 묶어서 새 dict생성
        # 리스트 컴프리핸션으로 생성
        create_user_dict = dict(filter(in_fields, self.cleaned_data.items()))

        # 람다함수를 사용
        create_user_dict = dict(filter(lambda item: item[0] in fields, self.cleaned_data.items()))

        user = User.objects.create_user(**create_user_dict)

        return user

        # 코드 줄이기 전에 사용했던 코드들
        # username = self.cleaned_data['username']
        # email = self.cleaned_data['email']
        # password = self.cleaned_data['password']
        # password2 = self.cleaned_data['password2']
        # site = self.cleaned_data['site']
        # introduce = self.cleaned_data['introduce']
        # img_profile = self.cleaned_data['img_profile']
        # gender = self.cleaned_data['gender']
        #
        # user = User.objects.create_user(
        #     username=username,
        #     email=email,
        #     password=password,
        #     site=site,
        #     introduce=introduce,
        #     img_profile=img_profile,
        #     gender=gender,
        #
        # )
        # return user
