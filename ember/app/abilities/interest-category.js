import { readOnly } from "@ember/object/computed";
import BaseAbility from "mysagw/abilities/-base";

export default class IdentityCategoryAbility extends BaseAbility {
  @readOnly("isStaff") canAdd;
  @readOnly("isStaff") canEdit;
  @readOnly("isStaff") canDelete;
}
