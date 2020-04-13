from rest_framework import serializers
from .models import FavoritePost


class CreateFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritePost
        fields = ['post', ]
