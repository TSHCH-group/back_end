from rest_framework import generics, permissions
from django.http import JsonResponse
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
    permission_classes = (permissions.IsAuthenticated,)
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


def increase_likes_of_post(request, pk):
    if request.user.is_authenticated():
        post = get_object_or_404(Post, pk=pk)
        try:
            obj = PostLikes.objects.get(post_id = pk, user_id = request.user.id)
        except:
            PostLikes.objects.create(post_id = post, user_id = request.user)
            post.number_of_likes = post.number_of_likes + 1
            post.save()
        return JsonResponse(post.number_of_likes)

    else:
        return JsonResponse("Authentication credentials not provided")
        
    