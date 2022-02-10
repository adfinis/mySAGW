import BaseAbility from "mysagw/abilities/-base";

export default class WorkItemAbility extends BaseAbility {
  get canList() {
    return this.isStaff;
  }
  get canEdit() {
    return this.isStaff;
  }
  get canShowAll() {
    return this.isStaff;
  }
}
