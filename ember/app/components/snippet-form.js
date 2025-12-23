import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

import applyError from "mysagw/utils/apply-error";

export default class SnippetFormComponent extends Component {
  @service notification;
  @service store;
  @service intl;

  @dropTask *submit(changeset) {
    try {
      yield changeset.save();

      this.notification.success(
        this.intl.t("components.snippet-form.success", {
          title: changeset.data.title,
        }),
      );

      this.args.onSave?.(changeset.data);
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
      applyError(changeset, error);
    }
  }
}
