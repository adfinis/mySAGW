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
