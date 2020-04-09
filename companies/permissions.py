from rest_framework import permissions


class DoesNotHaveCompanyOrDeny(permissions.BasePermission):
    message = "Only one company is allowed"

    def has_permission(self, request, view):
        return not hasattr(request.user, 'company')