import { readOnly } from "@ember/object/computed";
import BaseAbility from "mysagw/abilities/-base";

export default class InterestAbility extends BaseAbility {
  @readOnly("isStaff") canList;
  @readOnly("isStaff") canAdd;
  @readOnly("isStaff") canEdit;
  @readOnly("isStaff") canDelete;
}
