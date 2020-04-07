from rest_framework import generics, permissions
from .models import Post, Comment
from .serializers import (
    PostSerializerForList, CommentSerializerForCreate, CommentSerializerForList,
    CommentSerializerForDetail
)


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PostSerializerForList


class PostDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = ()


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializerForCreate

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentPostListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CommentSerializerForList


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = CommentSerializerForDetail
