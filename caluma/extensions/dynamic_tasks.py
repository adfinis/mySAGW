from caluma.caluma_workflow.dynamic_tasks import BaseDynamicTasks, register_dynamic_task
from caluma.caluma_workflow.models import WorkItem


def set_one_workitem_ready(query):
    is_ready = False
    for wi in query:
        wi.status = WorkItem.STATUS_CANCELED
        if not is_ready:
            wi.status = WorkItem.STATUS_READY
            is_ready = True
        wi.save()


class CustomDynamicTasks(BaseDynamicTasks):
    @register_dynamic_task("after-review-document")
    def resolve_after_review(self, case, user, prev_work_item, context):
        review_decision = prev_work_item.document.answers.get(
            question_id="review-document-decision",
        )

        if "reject" in review_decision.value:
            return ["revise-document"]
        if "continue" in review_decision.value:
            return ["circulation"]

        return []

    @register_dynamic_task("after-decision-and-credit")
    def resolve_after_decision_and_credit(self, case, user, prev_work_item, context):
        credit_decision = prev_work_item.document.answers.get(
            question_id="decision-and-credit-decision",
        )

        if "additional-data" in credit_decision.value:
            additional_data = case.work_items.filter(
                task__slug="additional-data",
                status=WorkItem.STATUS_REDO,
            )
            if additional_data.exists():
                set_one_workitem_ready(additional_data)
                return ["additional-data-form", "advance-credits"]

            return ["additional-data", "additional-data-form", "advance-credits"]
        if "define-amount" in credit_decision.value:
            define_amount = case.work_items.filter(
                task__slug="define-amount",
                status=WorkItem.STATUS_REDO,
            )
            if define_amount.exists():
                set_one_workitem_ready(define_amount)
                return []
            return ["define-amount"]

        return []

    @register_dynamic_task("after-define-amount")
    def resolve_after_define_amount(self, case, user, prev_work_item, context):
        decision = prev_work_item.document.answers.get(
            question_id="define-amount-decision",
        )

        if "reject" in decision.value:
            additional_data = case.work_items.filter(
                task__slug="additional-data",
                status=WorkItem.STATUS_REDO,
            )
            if additional_data.exists():
                set_one_workitem_ready(additional_data)
            return ["additional-data"]
        if "continue" in decision.value:
            return ["complete-document"]

        return []

    @register_dynamic_task("redo-define-amount")
    def redo_from_define_amount(self, case, user, prev_work_item, context):
        credit_decision = (
            case.work_items.filter(task_id="decision-and-credit")
            .order_by("-created_at")
            .first()
            .document.answers.get(
                question_id="decision-and-credit-decision",
            )
        )

        if "define-amount" in credit_decision.value:
            return ["decision-and-credit"]

        return []
