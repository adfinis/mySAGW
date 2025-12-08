import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "reactiveweb/function";
import UIkit from "uikit";

import getCancelledCases from "mysagw/gql/queries/get-cancelled-cases.graphql";
import applyError from "mysagw/utils/apply-error";
import IdentityValidations from "mysagw/validations/identity";

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
  @service can;
  @service apollo;

  @tracked backToIdentities;

  get changeset () {
    return this.changesetResource.value
  }

  changesetResource = trackedFunction(this, async () => {
    const identitiy = this.args.identity ?? this.store.createRecord("identity");
    // Prevent excessive re-rendering
    await Promise.resolve()
    return Changeset(
      identitiy,
      lookupValidator(IdentityValidations),
      IdentityValidations,
    );
  });

  get salutations() {
    return [
      { label: this.intl.t("global.salutation.neutral"), value: "neutral" },
      { label: this.intl.t("global.salutation.male"), value: "male" },
      { label: this.intl.t("global.salutation.female"), value: "female" },
    ];
  }

  get titles() {
    return [
      { label: this.intl.t("global.title.none"), value: "none" },
      { label: this.intl.t("global.title.dr"), value: "dr" },
      { label: this.intl.t("global.title.prof"), value: "prof" },
      { label: this.intl.t("global.title.profDr"), value: "prof-dr" },
      { label: this.intl.t("global.title.profEmDr"), value: "prof-em-dr" },
      { label: this.intl.t("global.title.pdDr"), value: "pd-dr" },
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
      "#/mysagw/users/",
      this.changeset?.get("idpId"),
      "/settings",
    ].join("");
  }

  get cancelRoute() {
    return this.args.cancelRouteOverride || "identities";
  }

  get disabledOnProfileView() {
    return (
      this.can.cannot("edit identity", this.changeset?.data) ||
      (this.changeset?.isOrganisation && this.args.profileView)
    );
  }

  @action
  eventTarget(handler, event) {
    handler(event.target.value);
  }

  @action
  updateOrganisation() {
    const isOrganisation = !this.changeset?.get("isOrganisation");
    this.args.onOrganisationUpdate?.(isOrganisation);
    this.changeset?.set("isOrganisation", isOrganisation);
  }

  @action
  setBackToIdentities() {
    this.backToIdentities = true;
    this.submit.perform(this.changeset);
  }

  @dropTask
  *submit(changeset) {
    try {
      if (!changeset.get("isOrganisation")) {
        changeset.set("organisationName", null);
        changeset.set("isExpertAssociation", false);
        changeset.set("isAdvisoryBoard", false);
      }

      yield changeset.save({
        adapterOptions: { customEndpoint: this.args.customEndpoint },
      });

      this.notification.success(
        this.intl.t("components.identity-form.success", {
          name: changeset.data.fullName,
        }),
      );

      this.args.onSave?.(changeset.data);

      if (this.backToIdentities) {
        this.router.transitionTo(this.cancelRoute);
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
      let message = this.intl.t("components.identity-form.delete.prompt");

      const accesses = yield this.store.query("case-access", {
        filter: { identityIds: this.args.identity.id },
      });

      const caseIds = accesses.map((access) => access.caseId);
      const cancelledCaseEdges = yield this.apollo.query(
        {
          query: getCancelledCases,
          variables: {
            caseIds,
          },
          fetchPolicy: "network-only",
        },
        "allCases.edges",
      );
      const casesNotCancelled = caseIds.filter(
        (caseId) =>
          !cancelledCaseEdges
            .map((edge) => decodeId(edge.node.id))
            .includes(caseId),
      );

      message += `\n${this.intl.t(
        "components.identity-form.delete.promptInfo",
        {
          caseAmount: casesNotCancelled.length,
        },
      )}`;

      const modal = UIkit.modal.confirm(message);
      // We need to add css white-space rule for the new line
      modal.dialog.$el.classList.add("white-space-pre-line");
      yield modal;

      try {
        yield identity.destroyRecord();
        this.notification.success(
          this.intl.t("components.identity-form.delete.success"),
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
