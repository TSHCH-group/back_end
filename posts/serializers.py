from rest_framework import serializers
from .models import Post, Comment
from django.conf import settings


class ImageUrlField(serializers.RelatedField):
    def to_representation(self, instance):
        url = instance.image.url
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)

        return url


class PostSerializerForList(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    profile_photo = serializers.ImageField(source='user.company.profile_photo', read_only=True)
    images = ImageUrlField(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'profile_photo', 'images', 'description', 'number_of_likes', 'creation_date']


class PostSerializerForDetail(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    images = ImageUrlField(read_only=True, many=True)
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'images', 'description', 'creation_date', 'update_date', 'comments']


class PostSerializerForCreate(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['description', 'images']


class CommentSerializerForCreate(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post_id', 'date', 'text']


class CommentSerializerForDetail(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']
