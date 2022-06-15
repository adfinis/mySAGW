import BaseAbility from "mysagw/abilities/-base";

export default class IdentityAbility extends BaseAbility {
  get canList() {
    return this.isStaff;
  }

  get canAdd() {
    return this.isStaff;
  }

  canEdit() {
    return this.isStaffOrOwnIdentity(this.model);
  }

  get canEditOrganisation() {
    return this.isStaff || this.model;
  }

  canAddInterest() {
    return this.isStaffOrOwnIdentity(this.model);
  }

  canRemoveInterest() {
    return this.isStaffOrOwnIdentity(this.model);
  }
}
