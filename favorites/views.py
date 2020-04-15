from rest_framework import generics, permissions
from .permissions import IsExist, IsPostExist, IsOwner
from .models import FavoritePost
from posts.models import Post
from .serializers import CreateFavoriteSerializer, ListFavoriteSerializer, UserDataSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import JsonResponse


class FavoriteCreateAPIView(generics.CreateAPIView):
    queryset = FavoritePost.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsExist)
    serializer_class = CreateFavoriteSerializer

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)


class FavoriteDestroyAPIView(generics.DestroyAPIView):
    queryset = FavoritePost.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsPostExist)
    serializer_class = CreateFavoriteSerializer

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        instance = FavoritePost.objects.get(user=self.request.user, post=post)
        self.perform_destroy(instance)


class FavoriteListAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDataSerializer
    lookup_field = 'username'


class UserInfo(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user_info = {
            "username": request.user.username,
            "email": request.user.email,
        }
        return JsonResponse(user_info)
