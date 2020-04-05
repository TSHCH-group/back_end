from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts')
    number_of_likes = models.PositiveIntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description



class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return self.text