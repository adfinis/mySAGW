import { attr, belongsTo } from "@ember-data/model";
import { LocalizedModel, localizedAttr } from "ember-localized-model";

export default class MembershipModel extends LocalizedModel {
  @belongsTo("identity") identity;
  @belongsTo("identity") organisation;
  @belongsTo("membership-role") role;
  @attr authorized;
  @attr timeSlot;
  @attr nextElection;
  @localizedAttr comment;
  @attr inactive;
}
