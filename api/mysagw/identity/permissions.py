from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, "is_admin", False)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, "is_staff", False)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAuthorized(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj in request.user.identity.authorized_for or (
            hasattr(obj, "identity")
            and (obj.identity in request.user.identity.authorized_for)
        )


class IsOwn(BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, "identity") and (obj.identity == request.user.identity)
