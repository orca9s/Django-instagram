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
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        site = self.cleaned_data['site']
        introduce = self.cleaned_data['introduce']
        img_profile = self.cleaned_data['img_profile']
        gender = self.cleaned_data['gender']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            site=site,
            introduce=introduce,
            img_profile=img_profile,
            gender=gender,

        )
        return user

    # 강사님이랑 하기전에 숙제로 한 부분
    # def clean_email(self):
    #
    #     email = self.cleaned_data['email']
    #     reputation = User.objects.filter(email=email).exists()
    #
    #     if reputation:
    #         raise ValidationError('이미 사용중인 이메일입니다.')
    #     return email
    #
    # def clean_password2(self):
    #     password = self.cleaned_data['password']
    #     password2 = self.cleaned_data['password2']
    #
    #     if password != password2:
    #         print('비밀번호가 일치하지 않습니다.')
    #         raise ValidationError('비밀번호가 일치하지 않습니다.')
    #     return password
