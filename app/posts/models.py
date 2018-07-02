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
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        # 1. related_name은 반대쪽(target)에서 이쪽(source)로의 연결을 만들어주는 Manager
        # 2. 자신이 like_users에 포함이 되는 Post QuerySet Manager
        # 3. -> 내가 좋아요 누른 Post목
        related_name='like_posts',
    )

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
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='my_users',
    )

    # parent_comment = models.ForeignKey(
    #     'self',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )

    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} : {self.content}'
