import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask } from "ember-concurrency-decorators";

import applyError from "mysagw/utils/apply-error";
import MembershipRoleValidations from "mysagw/validations/membership-role";

/**
 * @arg role
 * @arg onSave
 */
export default class MembershipRoleFormComponent extends Component {
  @service notification;
  @service store;
  @service intl;

  @tracked changeset;

  @action onUpdate() {
    this.changeset = Changeset(
      this.args.role || this.store.createRecord("membership-role"),
      lookupValidator(MembershipRoleValidations),
      MembershipRoleValidations
    );
  }

  @dropTask *submit(changeset) {
    try {
      yield changeset.save();
      this.notification.success(
        this.intl.t("component.membership-role-form.success", {
          role: changeset.data.title,
        })
      );
      this.args.onSave?.(changeset.data);
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
      applyError(changeset, error);
    }
  }
}
