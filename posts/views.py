from rest_framework import generics, permissions
from .models import Post, Comment
from .permissions import IsOwnerOrReadOnly, IsCompanyOrReadOnly
from .serializers import (
    PostSerializerForList,
    PostSerializerForDetail,
    PostSerializerForCreate,
    CommentSerializerForCreate,
    CommentSerializerForDetail,
)


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PostSerializerForList


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly, )
    serializer_class = PostSerializerForDetail


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsCompanyOrReadOnly, )
    serializer_class = PostSerializerForCreate

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializerForCreate

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = CommentSerializerForDetail
