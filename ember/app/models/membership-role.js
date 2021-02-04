import { attr } from "@ember-data/model";
import { LocalizedModel, localizedAttr } from "ember-localized-model";

export default class MembershipRoleModel extends LocalizedModel {
  @localizedAttr title;
  @localizedAttr description;
  @attr archived;
}
