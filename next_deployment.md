# Manual steps for next deployment

## Set meta on circulation work_items

Run in caluma shell:

```python
from caluma.extensions.api_client import APIClient
from caluma.caluma_workflow.models import WorkItem
from django.db import transaction


def get_user_props(idp_id):
    result = client.get(
        f"/identities?filter%5BidpIds%5D={idp_id}",
        token=token,
    )
    return result


client = APIClient()
token = client.get_admin_token()
work_items = WorkItem.objects.filter(task_id="circulation-decision")

with transaction.atomic():
    for work_item in work_items.iterator():
        if not work_item.assigned_users or (
            "assigneeName" in work_item.meta and "assigneeEmail" in work_item.meta
        ):
            # only set if unset
            continue
        user_props = get_user_props(work_item.assigned_users[0])
        if not user_props["data"]:
            print(f"{work_item.id} - no data")
            continue
        user_props = user_props["data"][0]["attributes"]
        work_item.meta[
            "assigneeName"
        ] = f'{user_props["last-name"]} {user_props["first-name"]}'
        work_item.meta["assigneeEmail"] = user_props["email"]
        print(work_item.id)
        work_item.save()
```