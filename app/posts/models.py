from django.conf import settings
from django.db import models

from members.models import User


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(upload_to='post', blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # 기본값은 오름차순인데 -를 붙이면 내림차순으로 정렬이 된다.
    # ordering
    class Meta:
        ordering = ['-pk']


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='my_comments',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_users',
    )

    content = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} : {self.content}'
