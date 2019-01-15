from rest_framework import permissions


class IsPublicOrSharedWithMe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' and obj.is_public:
            return True
        elif request.method in ['DELETE', 'PUT', 'PATCH'] and request.user == obj.owner:
            return True

        return (request.user in obj.shared_with.all()) or (request.user == obj.owner)
