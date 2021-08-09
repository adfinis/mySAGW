import { readOnly } from "@ember/object/computed";
import BaseAbility from "mysagw/abilities/-base";

export default class FormConfigurationAbility extends BaseAbility {
  @readOnly("isStaff") canList;
}
