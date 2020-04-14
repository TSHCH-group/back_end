from django.db import IntegrityError
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.http import JsonResponse, Http404
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Post, Comment, PostLikes
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
    permission_classes = (permissions.AllowAny,)
    serializer_class = PostSerializerForList
    pagination_class = PageNumberPagination
    PageNumberPagination.page_size = 10


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PostSerializerForDetail


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsCompanyOrReadOnly,)
    serializer_class = PostSerializerForCreate
    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


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


class PostLikesView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        post = self.get_object(pk)
        try:
            post_like = PostLikes.objects.create(post=post, user=request.user)
            post_like.save()
            post.number_of_likes = post.number_of_likes + 1
        except IntegrityError:
            post_like = PostLikes.objects.get(post=post, user=request.user)
            post_like.delete()
            post.number_of_likes = post.number_of_likes - 1
        post.save()
        return JsonResponse({"number_of_likes": post.number_of_likes})


