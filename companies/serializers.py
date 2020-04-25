from rest_framework import serializers
from .models import Company
from posts.models import Post, PostImages
from posts.serializers import ImageUrlField, PostSerializerForList


class CompanyCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name', 'profile_photo', 'background_photo', 'short_description', 'description', 'longitude',
                  'latitude']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = ['image', ]


class CompanyDetailSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    posts = PostSerializerForList(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    update_link = serializers.HyperlinkedIdentityField(view_name='update_company')

    class Meta:
        model = Company
        fields = ['company_name', 'profile_photo', 'background_photo', 'short_description', 'description',
                  'longitude', 'latitude', 'rating', 'is_owner', 'update_link', 'posts', ]

    def get_is_owner(self, obj):
        if self.context['request'].user == obj.user:
            return True
        return False

    def get_rating(self, obj):
        return calculate_rating(obj)


def calculate_rating(obj):
    queryset = obj.posts.all()
    dislikes = 0
    likes = 0
    for post in queryset:
        likes += post.number_of_likes
        dislikes += post.number_of_dislikes
    total = likes + dislikes
    if total == 0:
        return 0
    return likes * 100 / total


class CompanySearchSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['profile_photo', 'company_name', 'rating']

    def get_rating(self, obj):
        return calculate_rating(obj)
