import { attr, belongsTo } from "@ember-data/model";
import { LocalizedModel } from "ember-localized-model";
import moment from "moment";

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
    return this.timeSlot && this.timeSlot.upper
      ? this.inactive || moment().isAfter(this.timeSlot.upper, "day") > 0
      : this.inactive;
  }
}
