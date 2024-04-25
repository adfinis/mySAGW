import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { dropTask, restartableTask, lastValue } from "ember-concurrency";
import UIkit from "uikit";

export default class MembershipRolesIndexController extends Controller {
  @service notification;
  @service store;
  @service intl;

  // Lifecycle

  @action onUpdate() {
    this.fetchRoles.perform();
  }

  // List

  @lastValue("fetchRoles") roles;

  @restartableTask *fetchRoles() {
    try {
      return yield this.store.findAll("membership-role");
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @dropTask *delete(role) {
    try {
      const options = { role: role.title };
      yield UIkit.modal.confirm(
        this.intl.t("roles.index.delete.prompt", options),
      );

      try {
        yield role.destroyRecord();
        this.notification.success(
          this.intl.t("roles.index.delete.success", options),
        );
        this.onUpdate();
      } catch (error) {
        console.error(error);
        this.notification.fromError(error);
      }
    } catch (error) {
      // Dialog was dimissed. No action necessary.
      // Log the error anyway in case something else broke in the try.
      console.error(error);
    }
  }
}
