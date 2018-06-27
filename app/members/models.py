from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CHOICES_GENDER = {
        ('x', '선택안함'),
        ('m', '남성'),
        ('f', '여성'),
    }
    img_profile = models.ImageField(upload_to='user', blank=True)
    site = models.URLField(blank=True)
    introduce = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)

    def __str__(self):
        return self.username
