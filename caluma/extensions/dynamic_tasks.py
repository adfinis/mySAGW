from caluma.caluma_workflow.dynamic_tasks import BaseDynamicTasks, register_dynamic_task


class CustomDynamicTasks(BaseDynamicTasks):
    @register_dynamic_task("after-review-document")
    def resolve_after_review(self, case, user, prev_work_item, context):
        review_decision = prev_work_item.document.answers.get(
            question_id="review-document-decision",
        )

        if "reject" in review_decision.value:
            return ["revise-document"]
        elif "continue" in review_decision.value:
            return ["circulation"]

        return []

    @register_dynamic_task("after-decision-and-credit")
    def resolve_after_decision_and_credit(self, case, user, prev_work_item, context):
        credit_decision = prev_work_item.document.answers.get(
            question_id="decision-and-credit-decision",
        )

        if "additional-data" in credit_decision.value:
            return ["additional-data", "additional-data-form", "advance-credits"]
        elif "define-amount" in credit_decision.value:
            return ["define-amount"]
        elif "complete" in credit_decision.value:
            return ["complete-document"]

        return []

    @register_dynamic_task("after-define-amount")
    def resolve_after_define_amount(self, case, user, prev_work_item, context):
        decision = prev_work_item.document.answers.get(
            question_id="define-amount-decision",
        )

        if "reject" in decision.value:
            return ["additional-data"]

        return ["complete-document"]
