from django.http import JsonResponse
from rest_framework import status
from rest_framework import generics, permissions
from .models import FavoritePost
from .serializers import UserDataSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import JsonResponse


class FavoriteListAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDataSerializer
    lookup_field = 'username'


class CreateDestroyAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, pk):
        try:
            favorite = FavoritePost.objects.create(post_id=pk, user_id=request.user.id)
            favorite.save()
            return JsonResponse({'favorite': 'created'}, status=status.HTTP_201_CREATED)
        except:
            favorite = FavoritePost.objects.get(post_id=pk, user_id=request.user.id)
            favorite.delete()
            return JsonResponse({'favorite': 'destroyed'}, status=status.HTTP_200_OK)


class UserInfo(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user_info = {
            "username": request.user.username,
            "email": request.user.email,
        }
        return JsonResponse(user_info)
