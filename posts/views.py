from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializerForList

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PostSerializerForList


class PostDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = ()




