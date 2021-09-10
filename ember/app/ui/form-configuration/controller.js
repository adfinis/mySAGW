import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import calumaQuery from "ember-caluma/caluma-query";
import { allForms } from "ember-caluma/caluma-query/queries";
import { restartableTask, enqueueTask } from "ember-concurrency-decorators";

import saveFormMutation from "mysagw/gql/mutations/save-form.graphql";

export default class FormConfigurationController extends Controller {
  @service notification;
  @service intl;

  @queryManager apollo;

  @calumaQuery({ query: allForms })
  formQuery;

  @restartableTask
  *fetchForms() {
    yield this.formQuery.fetch({
      filter: [{ isPublished: true }, { isArchived: false }],
    });
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
        this.intl.t("form-configuration.saveSuccess", { name: form.name })
      );

      this.fetchForms.perform();
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }
}
