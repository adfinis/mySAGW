import BaseAbility from "mysagw/abilities/-base";

export default class IdentityCategoryAbility extends BaseAbility {
  get canAdd() {
    return this.isStaff;
  }
  get canEdit() {
    return this.isStaff;
  }
  get canDelete() {
    return this.isStaff;
  }
}
