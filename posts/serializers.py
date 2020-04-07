from rest_framework import serializers
from .models import Post, Comment


class PostSerializerForList(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'images', 'description', 'number_of_likes', 'creation_date']


class PostSerializerForDetail(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'description', 'number_of_likes', 'creation_date', 'update_date', 'comments']


class CommentSerializerForCreate(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post_id', 'date', 'text']


class CommentSerializerForList(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'user', 'date', 'text']


class CommentSerializerForDetail(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']
