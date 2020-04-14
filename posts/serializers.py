from rest_framework import serializers
from .models import Post, Comment
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
    company = serializers.CharField(source='company.company_name', read_only=True)
    profile_photo = serializers.ImageField(source='company.profile_photo', read_only=True)
    images = ImageUrlField(read_only=True, many=True)
    detail = serializers.HyperlinkedIdentityField(view_name='detail-post')
    add_to_favorite = serializers.HyperlinkedIdentityField(view_name='create-favorite')
    remove_from_favorites = serializers.HyperlinkedIdentityField(view_name='destroy-favorite')
    saved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'company', 'profile_photo', 'images',
                  'description', 'number_of_likes', 'creation_date', 'detail', 'add_to_favorite',
                  'remove_from_favorites', 'saved']

    def get_saved(self, ob):
        try:
            print(FavoritePost.objects.get(user_id=self.context['request'].user.id, post_id=ob.id))
        except:
            return False
        return True


class PostSerializerForDetail(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    images = ImageUrlField(read_only=True, many=True)
    comments = CommentSerializer(many=True)

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
