import json

import requests
from django.conf import settings


class CalumaClient:
    def __init__(
        self,
        token,
        endpoint,
    ):
        self.token = token
        self.endpoint = endpoint

    def execute(self, query, variables=None):
        return self._send(query, json.dumps(variables))

    def _send(self, query, variables):
        data = {"query": query, "variables": variables}
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self.token,
        }

        response = requests.post(
            self.endpoint, json=data, headers=headers, verify=settings.CALUMA_VERIFY_SSL
        )
        response.raise_for_status()
        return response.json()
