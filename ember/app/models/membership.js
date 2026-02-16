import { attr, belongsTo } from "@ember-data/model";
import { LocalizedModel } from "ember-localized-model";
import { DateTime } from "luxon";

const membershipInactive = (membership) => {
  return membership.inactive || membership.isExpired || membership.isInFuture;
};

export { membershipInactive };

export default class MembershipModel extends LocalizedModel {
  @belongsTo("identity", { inverse: "memberships", async: true }) identity;
  @belongsTo("identity", { inverse: "members", async: true }) organisation;
  @belongsTo("membership-role", { inverse: null, async: true }) role;
  @attr authorized;
  @attr timeSlot;
  @attr nextElection;
  @attr comment;
  @attr inactive;

  get isInactive() {
    return membershipInactive(this);
  }

  get isInFuture() {
    return (
      this.timeSlot?.lower &&
      DateTime.fromISO(this.timeSlot.lower) > DateTime.now()
    );
  }

  get isExpired() {
    return (
      this.timeSlot?.upper &&
      DateTime.now() > DateTime.fromISO(this.timeSlot.upper)
    );
  }
}
