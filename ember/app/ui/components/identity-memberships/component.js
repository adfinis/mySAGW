import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask, restartableTask, lastValue } from "ember-concurrency";
import moment from "moment";
import UIkit from "uikit";

import applyError from "mysagw/utils/apply-error";
import MembershipValidations from "mysagw/validations/membership";

/**
 * @arg identity
 */
export default class IdentityMembershipsComponent extends Component {
  @service store;
  @service intl;
  @service notification;

  // List

  @lastValue("fetchMemberships") memberships;
  @restartableTask
  *fetchMemberships(identity) {
    return yield this.store.query("membership", {
      filter: { identity: identity.id },
      include: "role",
    });
  }

  @action
  onUpdate() {
    this.fetchMemberships.perform(this.args.identity);
    this.fetchIdentities.perform(this.args.identity);
    this.fetchRoles.perform(this.args.identity);
  }

  @action
  openPowerSelect(select) {
    select.actions.open();
  }

  // Add / Edit

  @tracked changeset = null;

  @action
  edit(membership) {
    this.changeset = Changeset(
      membership ||
        this.store.createRecord("membership", {
          identity: this.args.identity,
          timeSlot: {},
        }),
      lookupValidator(MembershipValidations),
      MembershipValidations
    );

    if (!this.changeset.get("timeSlot")) {
      this.changeset.set("timeSlot", {});
    }
  }

  @action
  cancel() {
    this.changeset = null;
  }

  @dropTask
  *submit(changeset) {
    try {
      let timeSlot = changeset.get("timeSlot") || {};
      if (!timeSlot.lower && !timeSlot.upper) {
        timeSlot = null;
      } else {
        timeSlot.lower = timeSlot.lower
          ? moment(timeSlot.lower).format("YYYY-MM-DD")
          : undefined;
        timeSlot.upper = timeSlot.upper
          ? moment(timeSlot.upper).format("YYYY-MM-DD")
          : undefined;
      }
      changeset.set("timeSlot", timeSlot);

      const election = changeset.get("nextElection");
      if (election) {
        changeset.set("nextElection", moment(election).format("YYYY-MM-DD"));
      }

      yield changeset.save();
      this.changeset = null;
      yield this.onUpdate();
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
      applyError(changeset, error);
    }
  }

  @lastValue("fetchIdentities") identities;
  @restartableTask
  *fetchIdentities() {
    return yield this.store.query("identity", {
      filter: { isOrganisation: true },
    });
  }

  @lastValue("fetchRoles") roles;
  @restartableTask
  *fetchRoles() {
    return yield this.store.findAll("membership-role");
  }

  // Delete

  @dropTask
  *delete(membership) {
    try {
      const options = {
        membership: membership.get("organisation.organisationName"),
      };
      yield UIkit.modal.confirm(
        this.intl.t("components.identity-memberships.delete.prompt", options)
      );
      try {
        yield membership.destroyRecord();
        this.notification.success(
          this.intl.t("components.identity-memberships.delete.success", options)
        );
        yield this.onUpdate();
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
