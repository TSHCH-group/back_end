from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post


class FavoritePost(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorite_post')

    class Meta:
        unique_together = ('user', 'post')