# Manual steps for next deployment

## Change question type

Run in Caluma shell:

```python
from caluma.caluma_form.models import Question

q = Question.objects.get(slug="gesprochener-rahmenkredit")
ans = q.answers.all()

to_handle = []
for a in ans.iterator():
    try:
        float(a.value)
    except ValueError:
        to_handle.append(a)

assert not to_handle


for a in ans.iterator():
    try:
        a.value = float(a.value)
    except ValueError:
        to_handle.append(a)
    a.save()

q.type = Question.TYPE_FLOAT
q.save()
```

If you get an `AssertionError`, check the `to_handle`-list for answers that couldn't be
cast to `float` and manually handle them.


## Re-upload changed templates

```shell
docker-compose run --rm api python manage.py upload_template -t mysagw/accounting/templates/accounting-cover.docx
docker-compose run --rm api python manage.py upload_template -t mysagw/case/templates/credit-approval-de.docx
docker-compose run --rm api python manage.py upload_template -t mysagw/case/templates/credit-approval-fr.docx
docker-compose run --rm api python manage.py upload_template -t mysagw/case/templates/credit-approval-en.docx
```
