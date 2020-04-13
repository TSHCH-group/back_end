from rest_framework import permissions
from favorites.models import FavoritePost


class IsExist(permissions.BasePermission):
    message = "post already exist"

    def has_permission(self, request, view):
        try:
            FavoritePost.objects.get(user=request.user, post=view.kwargs["pk"])
        except:
            return True
        return False


class IsOwner(permissions.BasePermission):
    message = "You are not owner"

    def has_permission(self, request, view):
        try:
            FavoritePost.objects.get(user=request.user, post=view.kwargs["pk"])
        except:
            return False
        return True


class IsPostExist(permissions.BasePermission):
    message = "Does not exist"

    def has_permission(self, request, view):
        try:
            FavoritePost.objects.get(user=request.user, post=view.kwargs["pk"])
        except:
            return False
        return True
