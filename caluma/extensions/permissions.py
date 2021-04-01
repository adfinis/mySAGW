from caluma.caluma_core.mutation import Mutation
from caluma.caluma_core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)


class MySAGWPermission(BasePermission):
    def _is_admin_or_sagw(self, info):
        groups = info.context.user.groups
        return "admin" in groups or "sagw" in groups

    def _is_own(self, info, instance):
        return instance.created_by_user == info.context.user.username

    @permission_for(Mutation)
    def has_permission_fallback(self, mutation, info):
        return self._is_admin_or_sagw(info)

    @object_permission_for(Mutation)
    def has_object_permission_fallback(self, mutation, info, instance):
        return self._is_admin_or_sagw(info) or self._is_own(info, instance)
