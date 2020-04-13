from rest_framework import generics, permissions
from rest_framework.views import APIView
from .models import FavoritePost
from .serializers import CreateFavoriteSerializer


class FavoriteAPIView(APIView):
    def post(self, request, user_id):
        print('______________________________________')
        print(user_id)
        print('______________________________________')
