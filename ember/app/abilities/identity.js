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
  canAddInterest() {
    return this.isStaffOrOwnIdentity(this.model);
  }
  canRemoveInterest() {
    return this.isStaffOrOwnIdentity(this.model);
  }

  canEdit() {
    return this.isStaffOrOwnIdentity(this.model);
  }
}
