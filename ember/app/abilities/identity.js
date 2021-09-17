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
  canAddInterest(identity) {
    return this.isStaffOrOwnIdentity(identity);
  }
  canRemoveInterest(identity) {
    return this.isStaffOrOwnIdentity(identity);
  }

  canEdit(identity) {
    return this.isStaffOrOwnIdentity(identity);
  }
}
