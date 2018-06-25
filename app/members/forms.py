from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignupForm(forms.Form):
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

    def clean_username(self):

        username = self.cleaned_data['username']
        reputation = User.objects.filter(username=username).exists()

        if reputation:
            raise ValidationError('이미 사용중인 아이디입니다.')
        return username

    def clean_email(self):

        email = self.cleaned_data['email']
        reputation = User.objects.filter(email=email).exists()

        if reputation:
            raise ValidationError('이미 사용중인 이메일입니다.')
        return email

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            print('비밀번호가 일치하지 않습니다.')
            raise ValidationError('비밀번호가 일치하지 않습니다.')
        return password
