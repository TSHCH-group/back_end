from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializerForList

class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PostSerializerForList


