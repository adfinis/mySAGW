import BaseAbility from "mysagw/abilities/-base";

export default class MembershipRoleAbility extends BaseAbility {
  get canList() {
    return this.isStaff;
  }
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
