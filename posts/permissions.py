from rest_framework import permissions
from companies.models import Company

class IsOwnerOrReadOnly(permissions.BasePermission):
        message = "Only owner of this object can change it"

        def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True
            return obj.user == request.user


class IsCompanyOrReadOnly(permissions.BasePermission):
    message = "Only companies can create posts"

    def has_permission(self, request, view):
        return hasattr(request.user, 'company')