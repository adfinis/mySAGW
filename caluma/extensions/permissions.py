import urllib3
from django.conf import settings

from caluma.caluma_core.permissions import BasePermission
from caluma.caluma_form.storage_clients import client


class MySAGWPermission(BasePermission):
    def has_permission(self, mutation, info):
        return True


# FIXME: Remove once https://github.com/projectcaluma/caluma/pull/1408 is released
# This is an ugly hack, and only intended for local development! In
# Production, we will have proper certificates, so this won't be required.
if settings.DEBUG:
    urllib3.disable_warnings()
    client.client._http.connection_pool_kw["cert_reqs"] = "CERT_NONE"
