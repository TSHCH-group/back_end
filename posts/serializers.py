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


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['user', 'text', 'date']


class PostSerializerForList(serializers.ModelSerializer):
    company = serializers.CharField(source='company.company_name', read_only=True)
    profile_photo = serializers.ImageField(source='company.profile_photo', read_only=True)
    images = ImageUrlField(read_only=True, many=True)
    detail = serializers.HyperlinkedIdentityField(view_name='detail-post')
    add_to_favorite = serializers.HyperlinkedIdentityField(view_name='create-favorite')
    remove_from_favorites = serializers.HyperlinkedIdentityField(view_name='destroy-favorite')

    class Meta:
        model = Post
        fields = ['id', 'company', 'profile_photo', 'images',
                  'description', 'number_of_likes', 'creation_date', 'detail', 'add_to_favorite',
                  'remove_from_favorites']


class PostSerializerForDetail(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    images = ImageUrlField(read_only=True, many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'images', 'description', 'creation_date', 'update_date', 'comments']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = ['image', ]


class PostSerializerForCreate(serializers.HyperlinkedModelSerializer):
    images = ImageSerializer(source='postimages_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['description', 'images']

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        post = Post.objects.create(company=self.context.get('view').request.user.company, description=validated_data.get('description'))
        for image_data in images_data.values():
            PostImages.objects.create(post=post, image=image_data)
        return post


class CommentSerializerForCreate(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post_id', 'date', 'text']


class CommentSerializerForDetail(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']
