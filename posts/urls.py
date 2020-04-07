from django.urls import path
from .views import PostListAPIView, CommentCreateAPIView, CommentPostListAPIView, CommentDetailAPIView

urlpatterns = [
    path('', PostListAPIView.as_view()),
    path('comment/create/', CommentCreateAPIView.as_view()),
    path('comment/post/<int:post_id>/', CommentPostListAPIView.as_view()),
    path('comment/detail/<int:pk>/', CommentDetailAPIView.as_view())
]
