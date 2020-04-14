from django.urls import path
from .views import (
    FavoriteCreateAPIView,
    FavoriteDestroyAPIView,
    FavoriteListAPIView,
)

urlpatterns = [
    path('create/<int:pk>/', FavoriteCreateAPIView.as_view(), name='create-favorite'),
    path('destroy/<int:pk>/', FavoriteDestroyAPIView.as_view(), name='destroy-favorite'),
    path('list/<str:username>/', FavoriteListAPIView.as_view()),
]
