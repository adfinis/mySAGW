import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency-decorators";
import IdentityValidations from "mysagw/validations/identity";

/**
 * @arg identity
 * @arg onSave
 */
export default class IdentityFormComponent extends Component {
  @service notification;
  @service store;
  @service intl;

  @tracked model;

  validations = IdentityValidations;

  @action onUpdate() {
    this.model = this.args.identity || this.store.createRecord("identity");
  }

  @dropTask *submit(changeset) {
    try {
      changeset.execute();
      yield this.model.save();
      this.notification.success(
        this.intl.t("component.identity-form.success", {
          name: this.model.fullName,
        })
      );
      this.args.onSave?.(this.model);
    } catch (error) {
      console.error(error);
      this.notification.danger(error.message);
    }
  }
}
