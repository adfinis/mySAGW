import { readOnly } from "@ember/object/computed";
import BaseAbility from "mysagw/abilities/-base";

export default class FormBuilderAbility extends BaseAbility {
  @readOnly("isStaff") canList;
}
