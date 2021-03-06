from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from django.http import JsonResponse, Http404
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment, PostLikes, PostDislikes
from .permissions import IsOwnerOrReadOnly, IsCompanyOrReadOnly
from .serializers import (
    PostSerializerForList,
    PostSerializerForDetail,
    PostSerializerForCreate,
    CommentSerializer,
)


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.order_by('-creation_date')
    permission_classes = (permissions.AllowAny,)
    serializer_class = PostSerializerForList
    pagination_class = PageNumberPagination
    PageNumberPagination.page_size = 5


class PostDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PostSerializerForDetail


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsCompanyOrReadOnly,)
    serializer_class = PostSerializerForCreate

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, **kwargs)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, **kwargs):
        post = get_post(kwargs['pk'])
        serializer.save(user=self.request.user, post=post)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = CommentSerializer


def get_post(pk):
    try:
        return Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404


class PostLikesView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def put(self, request, pk):
        post = get_post(pk)
        is_liked = True
        try:
            post_disliked = PostDislikes.objects.get(post=post, user=request.user)
            post_disliked.delete()
            post.number_of_dislikes = post.number_of_dislikes - 1
            print('dislike deleted')
        except PostDislikes.DoesNotExist:
            pass

        try:
            post_like = PostLikes.objects.create(post=post, user=request.user)
            post_like.save()
            post.number_of_likes = post.number_of_likes + 1
        except IntegrityError:
            post_like = PostLikes.objects.get(post=post, user=request.user)
            post_like.delete()
            post.number_of_likes = post.number_of_likes - 1
            is_liked = False
        post.save()
        return JsonResponse({"number_of_likes": post.number_of_likes, 'is_liked': is_liked,
                             'number_of_dislikes': post.number_of_dislikes, 'is_disliked': False})


class PostDislikesView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def put(self, request, pk):
        post = get_post(pk)
        is_disliked = True
        try:
            post_liked = PostLikes.objects.get(post=post, user=request.user)
            post_liked.delete()
            post.number_of_likes = post.number_of_likes - 1
            print('Like deleted')
        except PostLikes.DoesNotExist:
            pass
        try:
            post_disliked = PostDislikes.objects.create(post=post, user=request.user)
            post_disliked.save()
            post.number_of_dislikes = post.number_of_dislikes + 1
        except IntegrityError:
            post_disliked = PostDislikes.objects.get(post=post, user=request.user)
            post_disliked.delete()
            post.number_of_dislikes = post.number_of_dislikes - 1
            is_disliked = False
        post.save()
        return JsonResponse({"number_of_likes": post.number_of_likes, 'is_liked': False,
                             'number_of_dislikes': post.number_of_dislikes, 'is_disliked': is_disliked})
