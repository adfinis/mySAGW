import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask } from "ember-concurrency-decorators";
import applyError from "mysagw/utils/apply-error";
import IdentityValidations from "mysagw/validations/identity";

/**
 * @arg identity
 * @arg onSave
 */
export default class IdentityFormComponent extends Component {
  @service notification;
  @service store;
  @service intl;

  @tracked changeset;

  get keyCloakAccountUrl() {
    const host =
      location.hostname === "localhost" ? "mysagw.local" : location.hostname;
    return [
      `https://${host}/auth/admin/master/console/`,
      "#/realms/mysagw/users/",
      this.changeset.get("idpId"),
    ].join("");
  }

  @action eventTarget(handler, event) {
    handler(event.target.value);
  }

  @action onUpdate() {
    this.changeset = Changeset(
      this.args.identity || this.store.createRecord("identity"),
      lookupValidator(IdentityValidations),
      IdentityValidations
    );
  }

  @dropTask *submit(changeset) {
    try {
      if (!changeset.get("isOrganisation")) {
        changeset.set("organisationName", null);
      }

      if (changeset.get("idpId")) {
        changeset.set("email", null);
      }

      yield changeset.save();
      this.notification.success(
        this.intl.t("component.identity-form.success", {
          name: changeset.data.fullName,
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
