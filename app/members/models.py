from django.contrib.auth.models import AbstractUser
from django.db import models

from members.exception import RelationNotExist


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
    to_relation_users = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
        blank=True,
        related_name='from_relation_users',
        related_query_name='from_relation_user',
    )

    def __str__(self):
        return self.username

    def follow(self, to_user):
        return self.relations_by_from_user.create(
            to_user=to_user,
            relation_type=Relation.RELATION_TYPE_FOLLOW

        )
        # Relation.objects.create(
        #     from_user=self,
        #     to_user=user,
        #     relation_type=Relation.RELATION_TYPE_FOLLOW,
        #
        # )

    def unfollow(self, to_user):
        # 아래 경우가 존재하면 실행
        # 존재하지 않으면
        q = self.relations_by_from_user.filter(
            to_user=to_user,
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )
        if q:
            q.delete()
        else:
            raise RelationNotExist(
                from_user=self,
                to_user=to_user,
                relation_type='Follow',
            )

    @property
    def following(self):
        # 내가 follow중인 User QuerySer리턴
        # hint __in=[<pk list>]
        # return User.objects.filter(
        #     pk__in=self.following_relations.values('to_user')
        # )
        return User.objects.filter(
            relations_by_to_user__from_user=self,
            relations_by_to_user__relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    @property
    def followers(self):
        # 나를 follow중인 User QuerySet
        # return User.objects.filter(
        #     pk__in=self.follower_relations.values('from_user')
        # )
        return User.objects.filter(
            relations_by_to_from__to_user=self,
            relations_by_to_from__relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    @property
    def block_users(self):
        # 내가 block중인 User QuerySet
        # return User.objects.filter(
        #     pk__in=self.block_relations.values('to_user')
        # )
        return User.objects.filter(
            relations_by_to_user__from_user=self,
            relations_by_to_user__relation_type=Relation.RELATION_TYPE_BLOCK,
        )

    @property
    def following_relations(self):
        # 내가 follow중인 Relation Query리턴
        return self.relations_by_from_user.filter(
            relation_type=Relation.RELATION_TYPE_FOLLOW
        )

    @property
    def follower_relations(self):
        # 나를 follow중인 Relation Query리턴
        return self.relations_by_to_user.filter(
            relation_type=Relation.RELATION_TYPE_FOLLOW
        )

    @property
    def block_relations(self):
        # 내가 block한 Relations Query리턴
        return self.relations_by_from_user.filter(
            relation_type=Relation.RELATION_TYPE_BLOCK
        )


class Relation(models.Model):
    """
    User간의 MTM연결 중계테이블
    """
    RELATION_TYPE_BLOCK = 'b'
    RELATION_TYPE_FOLLOW = 'f'
    CHOICES_RELATION_TYPE = (
        (RELATION_TYPE_FOLLOW, 'Follow'),
        (RELATION_TYPE_BLOCK, 'Block'),
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relations_by_from_user',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relations_by_to_user',
    )
    relation_type = models.CharField(max_length=1, choices=CHOICES_RELATION_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )

    def __str__(self):
        return 'From {from_user} to {to_user} ({type})'.format(
            from_user=self.from_user.username,
            to_user=self.to_user.username,
            type=self.get_relation_type_display(),
        )
