# Manual steps for next deployment


## Upload updated templates to DMS

```
docker compose run --rm api python manage.py upload_template \
    acknowledgement-de.docx \
    acknowledgement-fr.docx \
    acknowledgement-en.docx \
    credit-approval-de.docx \
    credit-approval-fr.docx \
    credit-approval-en.docx \
    application.docx
```

## Fix dangling circulations

```bash
docker compose run --rm caluma poetry run ./manage.py shell
```

```python
from caluma.caluma_workflow.models import Case, WorkItem

cases = Case.objects.filter(parent_work_item__isnull=True, document__form__slug="circulation-form")
print(f"Fixing {cases.count()} dangling circulations...")
for case in cases:
    for wi in case.work_items.all():
        wi.status = WorkItem.STATUS_CANCELED
        wi.save()
    case.status = Case.STATUS_CANCELED
    case.save()

print("Done.")
```
