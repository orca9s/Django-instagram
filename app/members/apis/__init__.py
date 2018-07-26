from rest_framework import generics

from ..models import User
from ..serializers import UserSerializer

__all__ = (
	'UserList',
)


class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer