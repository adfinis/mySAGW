# Manual steps for next deployment


### Fix case statuses

 - Remove status from Cases not stemming from the `document-review` Workflow
 - Set cancelled cases to `canceled`

Run in Caluma Django shell:

```python
from caluma.caluma_workflow.models import Case


def status_removal():
    cases = Case.objects.exclude(workflow__slug="document-review").filter(
        meta__status__isnull=False
    )
    print(f"Unset status of {cases.count()} Cases.")
    for case in cases:
        del case.meta["status"]
        case.save()


def set_cancelled_status():
    cases = Case.objects.filter(
        workflow__slug="document-review", status=Case.STATUS_CANCELED
    )
    print(f'Set status of {cases.count()} canceled Cases to "canceled".')
    for case in cases:
        case.meta["status"] = "canceled"
        case.save()


status_removal()
set_cancelled_status()

```
