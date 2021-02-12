import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import {
  dropTask,
  restartableTask,
  lastValue,
} from "ember-concurrency-decorators";
import MembershipValidations from "mysagw/validations/membership";
import UIkit from "uikit";

/**
 * @arg identity
 */
export default class IdentityMembershipsComponent extends Component {
  @service store;
  @service intl;
  @service notification;

  // List

  @lastValue("fetchMembership") memberships;

  @restartableTask *fetchMembership(identity) {
    return yield this.store.query("membership", {
      filter: { identity: identity.id },
      include: "role,organisation",
    });
  }

  @action onUpdate() {
    this.fetchMembership.perform(this.args.identity);
    this.fetchIdentities.perform(this.args.identity);
    this.fetchRoles.perform(this.args.identity);
  }

  // Add / Edit

  @tracked changeset = null;

  @action edit(membership) {
    this.changeset = Changeset(
      membership ||
        this.store.createRecord("membership", {
          identity: this.args.identity,
          timeSlot: {},
        }),
      lookupValidator(MembershipValidations),
      MembershipValidations
    );
  }

  @action cancel() {
    this.changeset = null;
  }

  @dropTask *submit(changeset) {
    try {
      yield changeset.save();

      this.changeset = null;
      yield this.onUpdate();
    } catch (error) {
      console.error(error);
      this.notification.danger(error.message);
    }
  }

  @lastValue("fetchIdentities") identities;

  @restartableTask *fetchIdentities() {
    return yield this.store.findAll("identity", {
      filter: { isOrganisation: true },
    });
  }

  @lastValue("fetchRoles") roles;

  @restartableTask *fetchRoles() {
    return yield this.store.findAll("membership-role");
  }

  // Delete

  @dropTask *delete(membership) {
    try {
      const options = {
        membership: membership.get("organisation.organisationName"),
      };
      yield UIkit.modal.confirm(
        this.intl.t("component.identity-memberships.delete.prompt", options)
      );
      try {
        yield membership.destroyRecord();
        this.notification.success(
          this.intl.t("component.identity-memberships.delete.success", options)
        );
        yield this.onUpdate();
      } catch (error) {
        console.error(error);
        this.notification.danger(error.message);
      }
    } catch (error) {
      // Dialog was dimissed. No action necessary.
    }
  }
}
