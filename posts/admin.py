from django.contrib import admin
from .models import Post, Comment, PostImages, PostLikes, PostDislikes
# Register your models here.


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostImagesInline(admin.TabularInline):
    model = PostImages
    extra = 0


class PostAdmin(admin.ModelAdmin):
    fields = ['company', 'description', 'number_of_likes', 'number_of_dislikes']
    inlines = [
        CommentInline,
        PostImagesInline,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostImages)
admin.site.register(PostLikes)
admin.site.register(PostDislikes)

