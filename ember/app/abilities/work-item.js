import { readOnly } from "@ember/object/computed";
import BaseAbility from "mysagw/abilities/-base";

export default class WorkItemAbility extends BaseAbility {
  @readOnly("isStaff") canEdit;
}
