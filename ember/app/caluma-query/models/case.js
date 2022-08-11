import { inject as service } from "@ember/service";
import CaseModel from "@projectcaluma/ember-core/caluma-query/models/case";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

import ENV from "mysagw/config/environment";

export default class CustomCaseModel extends CaseModel {
  @service store;

  get isRunning() {
    return this.raw.status === "RUNNING";
  }

  get isCompleted() {
    return this.raw.status === "COMPLETED";
  }

  get accesses() {
    return this.store.peekAll("case-access").filter((access) => {
      return (
        access.caseId === decodeId(this.raw.id) && !access.hasDirtyAttributes
      );
    });
  }

  get workItems() {
    return this.raw.workItems.edges
      .mapBy("node")
      .filter((workItem) => workItem.status !== "REDO");
  }

  get hasEditableWorkItem() {
    return this.workItems
      .filter((workItem) =>
        ENV.APP.caluma.documentEditableTaskSlugs.includes(workItem.task.slug)
      )
      .isAny("status", "READY");
  }

  get hasSubmitOrReviseWorkItem() {
    return this.workItems.find(
      (workItem) =>
        (workItem.task.slug === ENV.APP.caluma.submitTaskSlug ||
          workItem.task.slug === ENV.APP.caluma.reviseTaskSlug) &&
        workItem.status === "READY"
    );
  }

  get redoWorkItem() {
    if (this.canRedoWorkItem?.task.slug === "additional-data") {
      return this.workItems.find(
        (workItem) =>
          workItem.status === "COMPLETED" &&
          workItem.task.slug === "decision-and-credit"
      );
    }

    return this.workItems.find(
      (workItem) =>
        (workItem.status === "COMPLETED" || workItem.status === "SKIPPED") &&
        ENV.APP.caluma.redoableTaskSlugs.includes(workItem.task.slug)
    );
  }

  get canRedoWorkItem() {
    return this.workItems.find(
      (workItem) =>
        workItem.status === "READY" &&
        ENV.APP.caluma.canRedoTaskSlug.includes(workItem.task.slug)
    );
  }

  get completeWorkItem() {
    return this.workItems.findBy("task.slug", ENV.APP.caluma.completeTaskSlug);
  }

  get documentNumber() {
    return this.document.answers.edges.findBy(
      "node.question.slug",
      "dossier-nr"
    ).node.StringAnswerValue;
  }

  static fragment = `{
    id
    createdAt
    modifiedAt
    createdByUser
    closedAt
    status
    meta
    workItems(filter: [{status: REDO, invert: true}], order: [{attribute: CLOSED_AT, direction: DESC}]) {
      edges {
        node {
          id
          status
          createdAt
          closedAt
          task {
            slug
          }
          document {
            answers {
              edges {
                node {
                  ... on StringAnswer {
                    StringAnswerValue: value
                  }
                  ... on IntegerAnswer {
                    IntegerAnswerValue: value
                  }
                  ... on FloatAnswer {
                    FloatAnswerValue: value
                  }
                  question {
                    slug
                    label
                  }
                }
              }
            }
          }
        }
      }
    }
    document {
      id
      createdAt
      modifiedAt
      form {
        slug
        name
        description
      }
      answers(filter: [{ questions: ["dossier-nr", "verteilplan-nr"] }]) {
        edges {
          node {
            id
            question {
              slug
              ... on ChoiceQuestion {
                options {
                  edges {
                    node {
                      slug
                      label
                    }
                  }
                }
              }
            }
            ... on StringAnswer {
              StringAnswerValue: value
            }
          }
        }
      }
    }
  }`;
}
