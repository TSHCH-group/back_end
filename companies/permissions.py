from rest_framework import permissions


class DoesNotHaveCompanyOrDeny(permissions.BasePermission):
    message = "Only one company is allowed"

    def has_permission(self, request, view):
        return not hasattr(request.user, 'company')


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "Only owner of this object can change it"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
