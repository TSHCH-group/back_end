from django.urls import path
from .views import (
    FavoriteListAPIView,
    CreateDestroyAPIView,
)

urlpatterns = [
    path('save/or/del/<int:pk>/', CreateDestroyAPIView.as_view(), name='create-favorite'),
    path('list/', FavoriteListAPIView.as_view(), name='favorite_list'),
]
