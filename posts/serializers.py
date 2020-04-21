from rest_framework import serializers
from .models import Post, Comment, PostImages, PostLikes, PostDislikes
from favorites.models import FavoritePost


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
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    company = serializers.HyperlinkedRelatedField(view_name='company_detail', read_only=True)
    profile_photo = serializers.ImageField(source='company.profile_photo', read_only=True)
    images = ImageUrlField(read_only=True, many=True)
    detail = serializers.HyperlinkedIdentityField(view_name='detail-post')
    save_or_del = serializers.HyperlinkedIdentityField(view_name='create-favorite')
    post_saved = serializers.SerializerMethodField()
    like_link = serializers.HyperlinkedIdentityField(view_name='like')
    dislike_link = serializers.HyperlinkedIdentityField(view_name='dislike')
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    longitude = serializers.DecimalField(source='company.longitude', read_only=True, max_digits=9, decimal_places=6)
    latitude = serializers.DecimalField(source='company.latitude', read_only=True, max_digits=9, decimal_places=6)

    class Meta:
        model = Post
        fields = ['id', 'company_name', 'company', 'profile_photo', 'longitude', 'latitude', 'images',
                  'description', 'number_of_likes', 'creation_date', 'detail', 'save_or_del',
                  'post_saved', 'like_link', 'dislike_link', 'is_liked', 'is_disliked']

    def get_post_saved(self, ob):
        if not self.context['request'].user.is_authenticated:
            return False
        try:
            FavoritePost.objects.get(user=self.context['request'].user, post_id=ob)
            return True
        except FavoritePost.DoesNotExist:
            return False

    def get_is_liked(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        try:
            PostLikes.objects.get(user=self.context['request'].user, post=obj)
            return True
        except PostLikes.DoesNotExist:
            return False

    def get_is_disliked(self, obj):
        if self.get_is_liked(obj) or not self.context['request'].user.is_authenticated:
            return False
        try:
            PostDislikes.objects.get(post=obj, user=self.context['request'].user)
            return True
        except PostDislikes.DoesNotExist:
            return False



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
        post = Post.objects.create(company=self.context.get('view').request.user.company,
                                   description=validated_data.get('description'))
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
