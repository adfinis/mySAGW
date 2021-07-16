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

  get salutations() {
    return [
      { label: this.intl.t("global.salutation.neutral"), value: "neutral" },
      { label: this.intl.t("global.salutation.male"), value: "male" },
      { label: this.intl.t("global.salutation.female"), value: "female" },
    ];
  }

  get languages() {
    return [
      { label: this.intl.t("global.languages.german"), value: "de" },
      { label: this.intl.t("global.languages.english"), value: "en" },
      { label: this.intl.t("global.languages.french"), value: "fr" },
    ];
  }

  get keyCloakAccountUrl() {
    const host =
      location.hostname === "localhost" ? "mysagw.local" : location.hostname;

    if (this.args.customEndpoint === "me") {
      return `https://${host}/auth/realms/mysagw/account/#/personal-info`;
    }

    return [
      `https://${host}/auth/admin/mysagw/console/`,
      "#/realms/mysagw/users/",
      this.changeset.get("idpId"),
    ].join("");
  }

  get cancelRoute() {
    return this.args.cancelRouteOverride || "identities";
  }

  @action
  eventTarget(handler, event) {
    handler(event.target.value);
  }

  @action
  onUpdate() {
    this.changeset = Changeset(
      this.args.identity || this.store.createRecord("identity"),
      lookupValidator(IdentityValidations),
      IdentityValidations
    );
  }

  @action
  updateOrganisation() {
    const isOrganisation = !this.changeset.get("isOrganisation");
    this.args.onOrganisationUpdate?.(isOrganisation);
    this.changeset.set("isOrganisation", isOrganisation);
  }

  @action
  setBackToIdentities() {
    this.backToIdentities = true;
  }

  @dropTask
  *submit(changeset) {
    try {
      if (!changeset.get("isOrganisation")) {
        changeset.set("organisationName", null);
      }

      yield changeset.save({
        adapterOptions: { customEndpoint: this.args.customEndpoint },
      });

      this.notification.success(
        this.intl.t("component.identity-form.success", {
          name: changeset.data.fullName,
        })
      );
      this.args.onSave?.(changeset.data);

      if (this.backToIdentities) {
        this.router.transitionTo("identities");
      }
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
      applyError(changeset, error);
    }
  }

  @dropTask
  *delete(identity) {
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
