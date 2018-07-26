from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model
from .models import User



class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'pk',
			'username',
			'img_profile',
		)