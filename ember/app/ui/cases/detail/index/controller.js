import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import Changeset from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask, restartableTask } from "ember-concurrency-decorators";
import { saveAs } from "file-saver";

import ENV from "mysagw/config/environment";
import cancelCaseMutation from "mysagw/gql/mutations/cancel-case.graphql";
import CaseValidations from "mysagw/validations/case";

export default class CasesDetailIndexController extends Controller {
  @service router;
  @service notification;
  @service intl;

  @queryManager apollo;

  @tracked newRow;
  @tracked modalVisible;

  get readyWorkItems() {
    return this.model.workItems.filterBy("status", "READY").length;
  }

  get remarks() {
    return (
      this.model.workItems
        /*
         * This filters the queried workItems for only the ones
         * which contain answers to be displayed as configured in displayedAnswers
         * and the most recent workItem if there are multiple of the same task.
         */
        .reduce((workItems, workItem) => {
          if (
            !Object.keys(ENV.APP.caluma.displayedAnswers).includes(
              workItem.task.slug
            )
          ) {
            return workItems;
          } else if (!workItems.length) {
            return [...workItems, workItem];
          }

          if (new Date(workItem.createdAt) > new Date(workItems[0].createdAt)) {
            return [workItem];
          }

          return workItems;
        }, [])
        /*
         * This filters the answers of the workItem document,
         * only the configured answers in displayedAnswers should remain
         * and based on another configured questions answer the answer will be filtered or not
         */
        .map((workItem) => {
          return workItem.document.answers.edges.reduce(
            (filteredAnswers, answer, _, answers) => {
              Object.keys(ENV.APP.caluma.displayedAnswers).forEach(
                (taskSlug) => {
                  if (!workItem.task.slug.includes(taskSlug)) {
                    return;
                  }

                  const decision = answers.find(
                    (a) => a.node.question.slug === `${taskSlug}-decision`
                  );
                  const value =
                    decision.node[`${decision.node.__typename}Value`];

                  if (
                    ENV.APP.caluma.displayedAnswers[taskSlug][value].includes(
                      answer.node.question.slug
                    )
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
        })
        .flat()
    );
  }

  @dropTask
  *closeCase() {
    try {
      yield this.apollo.mutate({
        mutation: cancelCaseMutation,
        variables: { case: this.model.id },
      });

      this.notification.success(this.intl.t("documents.deleteSuccess"));

      this.router.transitionTo("cases.index");
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @action
  transtionToCases() {
    this.router.transtionTo("cases");
  }

  @action
  addAccessRow() {
    this.newRow = new Changeset(
      this.store.createRecord("case-access", {
        email: undefined,
        caseId: this.model.id,
      }),
      lookupValidator(CaseValidations),
      CaseValidations
    );

    this.modalVisible = true;
  }

  @restartableTask
  *saveAccessRow() {
    if (
      this.model.accesses.find((access) => {
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
    yield this.model.accesses.findBy("email", access.email).destroyRecord();

    if (this.can.cannot("list case", this.model)) {
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

    const uri = `${this.store.adapterFor("identity").buildURL("receipts")}/${
      this.model.id
    }`;
    const init = {
      method: "GET",
      headers: adapter.headers,
    };
    try {
      const response = yield fetch(uri, init);

      if (!response.ok) {
        throw new Error(response.statusText || response.status);
      }

      const blob = yield response.blob();
      const filename = `${this.intl.t("documents.accountingExportFilename", {
        dossierNo:
          this.model.document.answers.edges.firstObject.node.StringAnswerValue,
      })}`;

      saveAs(blob, filename);
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }
}
