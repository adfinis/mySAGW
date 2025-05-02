# Manual steps for next deployment

## Test client creds used by caluma

This can be tested from the shell, without modifying any data:

```python
from caluma.extensions.common import get_users_for_case
from caluma.caluma_workflow.models import Case

# Fetch the most recent case
c = Case.objects.filter(workflow__slug="document-review").order_by("-created_at").first()

# Fetch the users with access to this case from the API
get_users_for_case(c)

# This should return something like this:
# [
#     {
#         'idp-id': 'ID',
#         'email': 'MAIL',
#         'organisation-name': None,
#         'first-name':'Name',
#         'last-name': 'Name',
#         'salutation': 'neutral',
#         'language': 'de',
#         'is-organisation': False
#     }
# ]
```

## Test the monitoring config in Caddy

Make an authenticated request to the healthz endpoint from an IP that is configured in
the Caddy .env file. This should return the healthz information.

Do the same request from another IP and it should fail.

```bash
curl 'https://DOMAIN/api/v1/healthz' \
  -H 'Accept: application/vnd.api+json' \
  -H 'Authorization: Bearer $TOKEN' -v
```
