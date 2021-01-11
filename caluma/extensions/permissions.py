from caluma.caluma_core.permissions import BasePermission


class MySAGWPermission(BasePermission):
    def has_permission(self, mutation, info):
        return True
