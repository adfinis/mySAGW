import BaseAbility from "mysagw/abilities/-base";

export default class IdentityAbility extends BaseAbility {
  get canList() {
    return this.isStaff;
  }
  get canAdd() {
    return this.isStaff;
  }
  get canEditOrganisation() {
    return this.isStaff;
  }
  get canAddInterest() {
    return this.isStaff;
  }
  get canRemoveInterest() {
    return this.isStaff;
  }

  canEdit(identity) {
    return this.isStaffOrOwnIdentity(identity);
  }
}
