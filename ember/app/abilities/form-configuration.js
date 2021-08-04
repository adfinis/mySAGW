import BaseAbility from "mysagw/abilities/-base";

export default class FormConfigurationAbility extends BaseAbility {
  get canList() {
    return this.isStaff;
  }
}
