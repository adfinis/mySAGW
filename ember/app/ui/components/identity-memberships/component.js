import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask, restartableTask, lastValue } from "ember-concurrency";
import { DateTime } from "luxon";
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

  @action updateDateField(fieldName, newValue, changeset) {
    changeset.rollbackProperty(fieldName);
    changeset.set(fieldName, newValue);
  }

  @action
  openPowerSelect(select) {
    select.actions.open();
  }

  // Add / Edit

  @tracked changeset;

  @action
  edit(membership) {
    this.changeset = Changeset(
      membership ||
        this.store.createRecord("membership", {
          identity: this.args.identity,
          timeSlot: {},
        }),
      lookupValidator(MembershipValidations),
      MembershipValidations,
    );

    if (!this.changeset.get("timeSlot")) {
      this.changeset.set("timeSlot", {});
    }
  }

  @action
  cancel() {
    this.changeset = null;
  }

  formatDate(date) {
    // Flatpickr returns an array of dates.
    if (Array.isArray(date)) {
      return DateTime.fromJSDate(date[0]).toISODate();
    } else if (date) {
      return date;
    }
    return null;
  }

  @dropTask
  *submit(changeset) {
    try {
      changeset.execute();
      const timeSlot = new Map(Object.entries(changeset.data.timeSlot));
      timeSlot.forEach((slot) => {
        if (slot) {
          const [key, value] = slot;
          timeSlot[key] = this.formatDate(value);
        }
      });
      if (timeSlot.size) {
        changeset.set("timeSlot", Object.fromEntries(timeSlot));
      }
      const election = changeset.get("nextElection");
      changeset.set("nextElection", this.formatDate(election));
      changeset.set("timeSlot.bounds", "[)");
      yield changeset.validate();
      if (changeset.isValid) {
        yield changeset.save();
        yield this.onUpdate();
        this.changeset = null;
      }
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
      applyError(changeset, error);
      changeset.rollback();
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
        this.intl.t("components.identity-memberships.delete.prompt", options),
      );
      try {
        yield membership.destroyRecord();
        this.notification.success(
          this.intl.t(
            "components.identity-memberships.delete.success",
            options,
          ),
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
