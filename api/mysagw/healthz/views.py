from django.http import JsonResponse
from rest_framework.views import APIView
from watchman import settings as watchman_settings, views as watchman_views

from ..oidc_auth.permissions import IsAuthenticated, IsMonitoringMember


def _remove_keys(dictionary, keys):
    """
    Recursively remove given keys from dictionary.

    Copy/paste from caluma:
    https://github.com/projectcaluma/caluma/blob/main/caluma/caluma_core/views.py#L10
    """
    for key in keys:  # delete keys
        if key in dictionary:
            del dictionary[key]
    for value in dictionary.values():  # retrieve nested values
        if isinstance(value, dict):
            _remove_keys(value, keys)  # apply to dict
        if isinstance(value, list):
            [_remove_keys(v, keys) for v in value]  # apply to list


class HealthzView(APIView):
    permission_classes = (IsAuthenticated & IsMonitoringMember,)

    def get(self, request):
        checks, ok = watchman_views.run_checks(request)
        http_code = 200 if ok else watchman_settings.WATCHMAN_ERROR_CODE

        # Remove unwanted keys e.g. 'error', 'stacktrace'
        if not ok:
            _remove_keys(checks, ["error", "stacktrace"])

        return JsonResponse(checks, status=http_code)
