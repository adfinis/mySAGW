import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import Changeset from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask, restartableTask } from "ember-concurrency-decorators";

import ENV from "mysagw/config/environment";
import cancelCaseMutation from "mysagw/gql/mutations/cancel-case.graphql";
import redoWorkItemMutation from "mysagw/gql/mutations/redo-work-item.graphql";
import reopenCaseMutation from "mysagw/gql/mutations/reopen-case.graphql";
import downloadFile from "mysagw/utils/download-file";
import CaseValidations from "mysagw/validations/case";

export default class CasesDetailIndexController extends Controller {
  @service router;
  @service notification;
  @service intl;
  @service store;

  @queryManager apollo;

  @tracked newRow;
  @tracked modalVisible;
  @tracked isDeleteConfirmationShown = false;

  get readyWorkItems() {
    return this.case.workItems.filterBy("status", "READY").length;
  }

  /*
   * This filters the queried work items for only the ones
   * which contain answers to be displayed as configured in displayedAnswers
   * and the most recent workItem of them all.
   * Also returns the most recent of each alwaysDisplayedAnswers work item to the list.
   */
  get remarkWorkItems() {
    const configuredWorkItems = this.case.workItems
      .filter(
        (workItem) =>
          [
            ...Object.keys(ENV.APP.caluma.displayedAnswers),
            ...Object.keys(ENV.APP.caluma.alwaysDisplayedAnswers),
          ].includes(workItem.task.slug) && workItem.status === "COMPLETED"
      )
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

    const newestWorkItem = configuredWorkItems[0];

    const alwaysDisplayedWorkItem = Object.keys(
      ENV.APP.caluma.alwaysDisplayedAnswers
    )
      .map((slug) => configuredWorkItems.findBy("task.slug", slug))
      .compact();

    return { newest: newestWorkItem, always: alwaysDisplayedWorkItem };
  }

  /*
   * This filters the answers of the workItem document,
   * only the configured answers in displayedAnswers should remain
   * and based on another configured questions answer the answer will be filtered or not.
   * Answers in alwaysDisplayedAnswers should always be displayed.
   */
  get remarks() {
    const newestAnswer =
      this.remarkWorkItems.newest?.document.answers.edges.reduce(
        (filteredAnswers, answer, _, answers) => {
          Object.keys(ENV.APP.caluma.displayedAnswers).forEach((taskSlug) => {
            if (!this.remarkWorkItems.newest.task.slug.includes(taskSlug)) {
              return;
            }

            const decision = answers.find(
              (a) => a.node.question.slug === `${taskSlug}-decision`
            );
            const value = decision.node[`${decision.node.__typename}Value`];

            if (
              ENV.APP.caluma.displayedAnswers[taskSlug][value].includes(
                answer.node.question.slug
              ) &&
              answer.node[`${answer.node.__typename}Value`]
            ) {
              filteredAnswers.push({
                label: answer.node.question.label,
                value: answer.node[`${answer.node.__typename}Value`],
              });
            }
          });

          return filteredAnswers;
        },
        []
      );

    const alwaysDisplayedAnswers = this.remarkWorkItems.always.map(
      (workItem) => {
        return workItem.document.answers.edges.reduce(
          (filteredAnswers, answer) => {
            Object.keys(ENV.APP.caluma.alwaysDisplayedAnswers).forEach(
              (taskSlug) => {
                if (
                  ENV.APP.caluma.alwaysDisplayedAnswers[taskSlug].includes(
                    answer.node.question.slug
                  ) &&
                  answer.node[`${answer.node.__typename}Value`]
                ) {
                  filteredAnswers.push({
                    label: answer.node.question.label,
                    value: answer.node[`${answer.node.__typename}Value`],
                  });
                }
              }
            );

            return filteredAnswers;
          },
          []
        );
      }
    );

    return [...(newestAnswer ?? []), ...alwaysDisplayedAnswers].flat();
  }

  @dropTask
  *closeCase() {
    try {
      yield this.apollo.mutate({
        mutation: cancelCaseMutation,
        variables: { case: this.case.id },
      });

      this.isDeleteConfirmationShown = false;
      this.notification.success(this.intl.t("documents.deleteSuccess"));

      this.router.transitionTo("cases.index");
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @action
  transitionToCases() {
    this.router.transitionTo("cases");
  }

  @action
  addAccessRow() {
    this.newRow = new Changeset(
      this.store.createRecord("case-access", {
        email: undefined,
        caseId: this.case.id,
      }),
      lookupValidator(CaseValidations),
      CaseValidations
    );

    this.modalVisible = true;
  }

  @restartableTask
  *saveAccessRow() {
    if (
      this.case.accesses.find((access) => {
        return (
          (access.email ?? access.identity.get("email")) === this.newRow.email
        );
      })
    ) {
      this.notification.danger(
        this.intl.t("documents.accesses.duplicateEmail")
      );
      return;
    }

    if (this.newRow.isValid) {
      const email = this.newRow.email;

      this.newRow.save();

      yield this.store.query(
        "identity",
        { filter: { email } },
        { adapterOptions: { customEndpoint: "public-identities" } }
      );

      this.newRow = null;
      this.modalVisible = false;
    }
  }

  @dropTask
  *deleteAccessRow(access) {
    yield this.case.accesses.findBy("email", access.email).destroyRecord();

    if (this.can.cannot("list case", this.case)) {
      this.router.transitionTo("cases");
    }
  }

  @dropTask
  *cancelAccessRow() {
    yield this.newRow.destroyRecord();
    this.modalVisible = false;
  }

  @dropTask
  *exportAccounting() {
    const adapter = this.store.adapterFor("identity");

    const uri = `${adapter.buildURL("receipts")}/${this.case.id}`;
    const init = {
      method: "GET",
      headers: adapter.headers,
    };
    try {
      yield downloadFile(uri, init);
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @dropTask
  *redoLastWorkItem() {
    try {
      yield this.apollo.mutate({
        mutation: redoWorkItemMutation,
        variables: { input: { id: this.case.redoWorkItem.id } },
      });

      yield this.getCase.perform();

      this.notification.success(this.intl.t("documents.redoSuccess"));
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("documents.redoError"));
    }
  }

  @dropTask
  *reopenCase() {
    try {
      yield this.apollo.mutate({
        mutation: reopenCaseMutation,
        variables: {
          input: {
            id: this.case.id,
            workItems: [this.case.redoWorkItem.id],
          },
        },
      });

      yield this.getCase.perform();

      this.notification.success(this.intl.t("documents.reopenSuccess"));
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("documents.reopenError"));
    }
  }

  @calumaQuery({ query: allCases })
  caseQuery;

  @dropTask
  *getCase() {
    yield this.caseQuery.fetch({ filter: [{ id: this.model.id }] });
  }

  get case() {
    return this.caseQuery.value.firstObject ?? this.model;
  }
}
