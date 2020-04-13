from django.urls import path
from .views import (
    FavoriteAPIView
)

urlpatterns = [
    path('<int:post_id>/', FavoriteAPIView.as_view()),
]
