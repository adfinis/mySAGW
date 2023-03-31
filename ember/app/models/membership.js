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
  @belongsTo("identity") identity;
  @belongsTo("identity") organisation;
  @belongsTo("membership-role") role;
  @attr authorized;
  @attr timeSlot;
  @attr nextElection;
  @attr comment;
  @attr inactive;

  get isInactive() {
    return membershipInactive(this);
  }
}
