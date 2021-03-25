import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask } from "ember-concurrency-decorators";
import applyError from "mysagw/utils/apply-error";
import IdentityValidations from "mysagw/validations/identity";
import UIkit from "uikit";

/**
 * @arg identity
 * @arg onSave
 * @arg onOrganisationUpdate
 */
export default class IdentityFormComponent extends Component {
  @service notification;
  @service store;
  @service intl;
  @service router;

  @tracked changeset;

  get keyCloakAccountUrl() {
    const host =
      location.hostname === "localhost" ? "mysagw.local" : location.hostname;
    return [
      `https://${host}/auth/admin/mysagw/console/`,
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

  @action updateOrganisation() {
    const isOrganisation = !this.changeset.get("isOrganisation");
    this.args.onOrganisationUpdate?.(isOrganisation);
    this.changeset.set("isOrganisation", isOrganisation);
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

  @dropTask *delete(identity) {
    try {
      yield UIkit.modal.confirm(
        this.intl.t("component.identity-form.delete.prompt")
      );

      try {
        yield identity.destroyRecord();
        this.notification.success(
          this.intl.t("component.identity-form.delete.success")
        );
        this.router.transitionTo("identities");
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
