import BaseAbility from "mysagw/abilities/-base";

export default class FormBuilderAbility extends BaseAbility {
  get canList() {
    return this.isStaff;
  }
}
