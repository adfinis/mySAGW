import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | cases/detail/index", function (hooks) {
  setupTest(hooks);

  test("it computes remarks", function (assert) {
    const controller = this.owner.lookup("controller:cases/detail/index");
    controller.model = {
      workItems: [
        {
          __typename: "WorkItem",
          id: "V29ya0l0ZW06N2RhNTlhZjAtMDUzMC00OGY2LWEwMzItY2U3ODcwZDg4MGZk",
          status: "READY",
          createdAt: "2023-03-03T09:27:58.795277+00:00",
          closedAt: null,
          task: {
            __typename: "SimpleTask",
            slug: "complete-document",
          },
          document: null,
        },
        {
          __typename: "WorkItem",
          id: "V29ya0l0ZW06YTllYzE3MzctMWZmOS00YjNhLWI5NTEtM2MyYWQwYzJjOWRl",
          status: "COMPLETED",
          createdAt: "2023-02-22T08:08:13.312479+00:00",
          closedAt: "2023-03-03T09:29:41.249101+00:00",
          task: {
            __typename: "CompleteTaskFormTask",
            slug: "define-amount",
          },
          document: {
            __typename: "Document",
            answers: {
              __typename: "AnswerConnection",
              edges: [
                {
                  __typename: "AnswerEdge",
                  node: {
                    __typename: "StringAnswer",
                    question: {
                      __typename: "ChoiceQuestion",
                      meta: {},
                      slug: "define-amount-decision",
                      label: "Entscheid",
                    },
                    StringAnswerValue: "define-amount-decision-continue",
                  },
                },
                {
                  __typename: "AnswerEdge",
                  node: {
                    __typename: "FloatAnswer",
                    question: {
                      __typename: "FloatQuestion",
                      meta: {},
                      slug: "define-amount-amount-float",
                      label: "Betrag",
                    },
                    FloatAnswerValue: 1234,
                  },
                },
                {
                  __typename: "AnswerEdge",
                  node: {
                    __typename: "StringAnswer",
                    question: {
                      __typename: "TextareaQuestion",
                      meta: {},
                      slug: "define-amount-remark",
                      label: "Kommentar",
                    },
                    StringAnswerValue: "Remarked",
                  },
                },
              ],
            },
          },
        },
        {
          __typename: "WorkItem",
          id: "V29ya0l0ZW06YjVlZmI5ZGEtNDcyMi00NjllLTliYWMtZTBiYWMzNzljYTFj",
          status: "COMPLETED",
          createdAt: "2023-02-22T07:24:01.560319+00:00",
          closedAt: "2023-02-22T08:08:13.250799+00:00",
          task: {
            __typename: "CompleteTaskFormTask",
            slug: "decision-and-credit",
          },
          document: {
            __typename: "Document",
            answers: {
              __typename: "AnswerConnection",
              edges: [
                {
                  __typename: "AnswerEdge",
                  node: {
                    __typename: "StringAnswer",
                    question: {
                      __typename: "TextQuestion",
                      meta: {
                        waehrung: "chf",
                      },
                      slug: "gesprochener-rahmenkredit",
                      label: "Gesprochener Rahmenkredit",
                    },
                    StringAnswerValue: "123",
                  },
                },
                {
                  __typename: "AnswerEdge",
                  node: {
                    __typename: "StringAnswer",
                    question: {
                      __typename: "ChoiceQuestion",
                      meta: {},
                      slug: "decision-and-credit-decision",
                      label: "Entscheid",
                    },
                    StringAnswerValue:
                      "decision-and-credit-decision-define-amount",
                  },
                },
              ],
            },
          },
        },
        {
          __typename: "WorkItem",
          id: "V29ya0l0ZW06ZmVjMDE2MDctMTJlMS00MTliLTkwZGEtMzE5NGE4NDM3ZWNk",
          status: "SKIPPED",
          createdAt: "2023-02-22T07:23:57.190348+00:00",
          closedAt: "2023-02-22T07:24:01.495012+00:00",
          task: {
            __typename: "SimpleTask",
            slug: "circulation",
          },
          document: null,
        },
        {
          __typename: "WorkItem",
          id: "V29ya0l0ZW06NjlhMmY2OGEtODQ1My00MmY2LWExMGUtYmFmZjlkZjc5ZDMx",
          status: "COMPLETED",
          createdAt: "2023-02-22T07:22:07.484960+00:00",
          closedAt: "2023-02-22T07:23:57.156593+00:00",
          task: {
            __typename: "CompleteTaskFormTask",
            slug: "review-document",
          },
          document: {
            __typename: "Document",
            answers: {
              __typename: "AnswerConnection",
              edges: [
                {
                  __typename: "AnswerEdge",
                  node: {
                    __typename: "StringAnswer",
                    question: {
                      __typename: "ChoiceQuestion",
                      meta: {},
                      slug: "review-document-decision",
                      label: "Entscheid",
                    },
                    StringAnswerValue: "review-document-decision-continue",
                  },
                },
              ],
            },
          },
        },
        {
          __typename: "WorkItem",
          id: "V29ya0l0ZW06ODgyMjFiY2YtNzNmYy00OGVkLTgyNDUtZTYxYzVkMGQ0Zjk0",
          status: "COMPLETED",
          createdAt: "2023-02-07T12:12:39.175257+00:00",
          closedAt: "2023-02-22T07:22:07.413257+00:00",
          task: {
            __typename: "CompleteWorkflowFormTask",
            slug: "submit-document",
          },
          document: null,
        },
      ],
    };

    assert.deepEqual(controller.remarks, [
      {
        label: "Betrag",
        value: 1234,
      },
      {
        label: "Kommentar",
        value: "Remarked",
      },
      {
        label: "Gesprochener Rahmenkredit",
        value: "CHF 123.-",
      },
    ]);
  });
});
