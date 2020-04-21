from django.urls import path
from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostCreateAPIView,
    CommentCreateAPIView,
    CommentDetailAPIView,
    PostLikesView,
    PostDislikesView,
)
urlpatterns = [
    path('', PostListAPIView.as_view()),
    path('post/create/', PostCreateAPIView.as_view()),
    path('post/detail/<int:pk>/', PostDetailAPIView.as_view(), name='detail-post'),
    path('comment/create/', CommentCreateAPIView.as_view()),
    path('comment/detail/<int:pk>/', CommentDetailAPIView.as_view()),
    path('post/<int:pk>/liked/', PostLikesView.as_view(), name='like'),
    path('post/<int:pk>/disliked/', PostDislikesView.as_view(), name='dislike'),
]
