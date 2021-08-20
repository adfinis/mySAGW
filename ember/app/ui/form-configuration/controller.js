import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import {
  lastValue,
  restartableTask,
  enqueueTask,
} from "ember-concurrency-decorators";

import saveFormMutation from "mysagw/gql/mutations/save-form.graphql";
import getRootFormsQuery from "mysagw/gql/queries/get-root-forms.graphql";

export default class FormConfigurationController extends Controller {
  @service notification;
  @service intl;

  @queryManager apollo;

  @lastValue("fetchForms") forms;
  @restartableTask
  *fetchForms() {
    const forms = yield this.apollo.query(
      {
        query: getRootFormsQuery,
        variables: { filter: [{ isPublished: true }, { isArchived: false }] },
        fetchPolicy: "network-only",
      },
      "allForms.edges"
    );

    return forms.mapBy("node");
  }

  @enqueueTask
  *setFormMeta(form, formType) {
    try {
      const meta = Object.assign({}, form.meta);

      if (meta[formType]) {
        delete meta[formType];
      } else {
        meta[formType] = true;
      }

      yield this.apollo.mutate({
        mutation: saveFormMutation,
        variables: {
          input: {
            slug: form.slug,
            name: form.name,
            meta: JSON.stringify(meta),
          },
        },
      });

      this.notification.success(
        this.intl.t("page.form-configuration.saveSuccess", { name: form.name })
      );

      this.fetchForms.perform();
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }
}
