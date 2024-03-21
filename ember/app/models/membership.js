import { attr, belongsTo } from "@ember-data/model";
import { LocalizedModel } from "ember-localized-model";
import { DateTime } from "luxon";

const membershipInactive = (membership) => {
  return membership.timeSlot && membership.timeSlot.upper
    ? membership.inactive ||
        DateTime.now() > DateTime.fromISO(membership.timeSlot.upper)
    : membership.inactive;
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
}
