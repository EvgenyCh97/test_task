from rest_framework.permissions import BasePermission


class IsSameUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in ['GET', 'POST']

    def has_object_permission(self, request, view, obj):
        if (request.method in ['PATCH', 'PUT', 'DELETE'] and
                request.user.is_authenticated):
            return request.user == obj
        return True


class IsFileOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method == 'GET'

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and
                (request.method == 'GET' or request.user == obj.owner))
