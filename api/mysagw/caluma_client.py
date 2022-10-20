import json
from base64 import urlsafe_b64encode

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

    def get_data(self, case_id, gql_file):
        with gql_file.open("r") as f:
            query = f.read()
        global_id = urlsafe_b64encode(f"Case:{case_id}".encode("utf-8")).decode("utf-8")
        variables = {"case_id": global_id}
        resp = self.execute(query, variables)
        return resp
