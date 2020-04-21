from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = "Only owner of this object can change it"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerUser(permissions.BasePermission):
    message = "Only the owner of this username can see"

    def has_object_permission(self, request, view, obj):
        return view.kwargs["username"] == request.user.username
