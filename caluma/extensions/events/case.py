from django.db import transaction

from caluma.caluma_core.events import on
from caluma.caluma_workflow import api as caluma_workflow_api
from caluma.caluma_workflow.events import post_complete_case


@on(post_complete_case, raise_exception=True)
@transaction.atomic
def complete_circulation(sender, case, user, **kwargs):
    if case.workflow_id == "circulation":
        caluma_workflow_api.complete_work_item(
            work_item=case.parent_work_item, user=user
        )
