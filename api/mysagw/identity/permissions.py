from rest_framework.permissions import BasePermission


class IsAuthorized(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj in request.user.identity.authorized_for or (
            hasattr(obj, "identity")
            and (obj.identity in request.user.identity.authorized_for)
        )


class IsOwn(BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, "identity") and (obj.identity == request.user.identity)
