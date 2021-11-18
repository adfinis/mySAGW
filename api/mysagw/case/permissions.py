from rest_framework.permissions import BasePermission

from mysagw.case.models import CaseAccess


class HasCaseAccess(BasePermission):
    def _has_access_to_case(self, identity, case_id):
        return CaseAccess.objects.filter(case_id=case_id, identity=identity).exists()

    def has_permission(self, request, view):
        if request.method in ["DELETE", "GET"]:
            return True
        return self._has_access_to_case(request.user.identity, request.data["case_id"])

    def has_object_permission(self, request, view, obj):
        return self._has_access_to_case(request.user.identity, obj.case_id)
