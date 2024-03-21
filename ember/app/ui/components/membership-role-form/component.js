import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask } from "ember-concurrency";

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
  @service router;

  @tracked changeset;
  @tracked backToRoles;

  @action
  onUpdate() {
    this.changeset = Changeset(
      this.args.role || this.store.createRecord("membership-role"),
      lookupValidator(MembershipRoleValidations),
      MembershipRoleValidations,
    );
  }

  @action
  setBackToRoles(event) {
    event.preventDefault();
    this.backToRoles = true;
    this.submit.perform(this.changeset);
  }

  @dropTask
  *submit(changeset) {
    try {
      yield changeset.save();
      this.notification.success(
        this.intl.t("components.membership-role-form.success", {
          role: changeset.title,
        }),
      );

      this.args.onSave?.(changeset);

      if (this.backToRoles) {
        this.router.transitionTo("membership-roles");
      }
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
      applyError(changeset, error);
    }
  }
}
