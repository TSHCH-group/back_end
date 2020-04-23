from rest_framework import serializers
from .models import Company
from posts.models import Post, PostImages
from posts.serializers import ImageUrlField


class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name', 'profile_photo', 'background_photo', 'short_description', 'description', 'longitude',
                  'latitude']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = ['image', ]


class PostSerializer(serializers.ModelSerializer):
    post_detail = serializers.HyperlinkedIdentityField(view_name='detail-post')
    images = ImageUrlField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['post_detail', 'images']


class CompanyDetailSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['company_name', 'profile_photo', 'background_photo', 'short_description', 'description',
                  'longitude', 'latitude', 'posts', 'is_owner']

    def get_is_owner(self, obj):
        if self.context['request'].user == obj.user:
            return True
        return False


class CompanySearchSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['profile_photo', 'company_name', 'rating']

    def get_rating(self, obj):
        likes = obj.number_of_likes
        dislikes = obj.number_of_dislikes
        all = likes + dislikes
        if all == 0:
            return 0
        return likes * 100 / all
