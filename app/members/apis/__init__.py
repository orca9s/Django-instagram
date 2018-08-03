from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User
from ..serializers import UserSerializer

__all__ = (
	'UserList',
)


class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class AuthToken(APIView):
	def post(self, request):
		serializer = AuthTokenSerializer(data=request.data)

		if serializer.is_valid(raise_exception=True):
			user = serializer.validated_data['user']
			token, _= Token.objects.get_or_create(user=user)

			data = {
				'token' : token.key,
			}

			return Response(data, status=status.HTTP_200_OK)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
