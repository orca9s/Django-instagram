from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # 초이스 젠더 성별 선택지 만들어줌
    CHOICES_GENDER = {
        ('x', '선택안함'),
        ('m', '남성'),
        ('f', '여성'),
    }
    img_profile = models.ImageField(upload_to='user', blank=True)
    site = models.URLField(blank=True)
    introduce = models.TextField(blank=True)
    # gender는 초이스 젠더를 가져옴
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)

    def __str__(self):
        return self.username
