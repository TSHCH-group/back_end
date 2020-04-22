from django.db import IntegrityError
from rest_framework import status
from rest_framework import generics, permissions
from .models import FavoritePost
from .serializers import UserDataSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response


class FavoriteListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        serializer = UserDataSerializer(user, context={'request': request})
        return Response(serializer.data)


class CreateDestroyAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "You have to login"}, status=status.HTTP_403_FORBIDDEN)
        try:
            favorite = FavoritePost.objects.create(post_id=pk, user_id=request.user.id)
            favorite.save()
            return JsonResponse({'favorite': True}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            favorite = FavoritePost.objects.get(post_id=pk, user_id=request.user.id)
            favorite.delete()
            return JsonResponse({'favorite': False}, status=status.HTTP_200_OK)
