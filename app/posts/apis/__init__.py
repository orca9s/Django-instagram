# /api/posts/
# 1. posts.serializers -> PostSerializer
# 2. apis.__init__
#	class PostList(APIView):
#		def get(self, request):
#			<logic>

# 3. config.urls에서 (posts.urls는 무시)
#	/pai/posts/ 가 위의 PostList.as_view()와 연결되도록 하라
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Post
from ..serializers import PostSerializer

__all__ = (
	'PostList',
)


# class PostList(APIView):
# 	def get(self, request):
# 		posts = Post.objects.all()
# 		serializer = PostSerializer(posts, many=True)
# 		return Response(serializer.data)

class PostList(generics.ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
