from django.contrib import admin
from .models import Post, Comment
# Register your models here.


class CommentInline(admin.TabularInline): # new
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin): # new
    inlines = [
        CommentInline,
    ]


admin.site.register(Post, PostAdmin) # new
admin.site.register(Comment)

