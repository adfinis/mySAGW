# Manual steps for next deployment

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
