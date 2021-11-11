import BaseAbility from "mysagw/abilities/-base";

export default class CaseAbility extends BaseAbility {
  get canExportForAccounting() {
    return this.isStaff;
  }
}
