from rest_framework import serializers
from .models import Post

class PostSerializerForList(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'description', 'number_of_likes', 'creation_date']


class PostSerializerForDetail(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'description', 'number_of_likes', 'creation_date', 'update_date', 'comments']
