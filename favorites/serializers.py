from rest_framework import serializers
from .models import FavoritePost
from django.contrib.auth.models import User


class ListFavoriteSerializer(serializers.ModelSerializer):
    post = serializers.HyperlinkedRelatedField(read_only=True, view_name='detail-post')

    class Meta:
        model = FavoritePost
        fields = ['post']


class UserDataSerializer(serializers.ModelSerializer):
    favorites = ListFavoriteSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'favorites']
