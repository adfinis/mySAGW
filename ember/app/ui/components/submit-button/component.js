import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { lastValue, restartableTask } from "ember-concurrency";

import ENV from "mysagw/config/environment";
import getDocumentsQuery from "mysagw/gql/queries/get-documents.graphql";

export default class SubmitButtonComponent extends Component {
  @service router;
  @service notification;
  @service intl;

  @queryManager apollo;

  @lastValue("fetchWorkItem") workItem;
  @restartableTask
  *fetchWorkItem() {
    const document = yield this.apollo.query(
      {
        query: getDocumentsQuery,
        variables: { filter: [{ id: this.args.field.document.uuid }] },
      },
      "allDocuments.edges"
    );

    return document
      .mapBy("node")[0]
      .case.workItems.edges.mapBy("node")
      .find((workItem) => {
        return (
          workItem.status === "READY" &&
          (workItem.task.slug === ENV.APP.caluma.submitTaskSlug ||
            workItem.task.slug === ENV.APP.caluma.reviseTaskSlug)
        );
      });
  }

  @action
  validationError() {
    this.notification.danger(this.intl.t("components.submit-button.error"));
  }

  @action
  transitionToCase() {
    this.router.transitionTo("cases");
  }
}
