import BaseAbility from "mysagw/abilities/-base";

export default class CaseAbility extends BaseAbility {
  get canExportForAccounting() {
    return this.isStaff;
  }
  get canList() {
    return this.isInvited(this.model) || this.isStaff;
  }
  get canEdit() {
    return this.isInvited(this.model);
  }
}
