# Manual steps for next deployment

## Upload new template version to DMS

```bash
docker compose run --rm api python manage.py upload_template acknowledgement-de.docx \
    acknowledgement-fr.docx acknowledgement-en.docx credit-approval-de.docx \
    credit-approval-fr.docx credit-approval-en.docx
   ```

## Set `OIDC_RP_CLIENT_USERNAME` setting

The env var `OIDC_RP_CLIENT_GRANT_VALUE` to set `OIDC_RP_CLIENT_USERNAME` must be set to
the correct client username: `service-account-caluma_admin_client`.
