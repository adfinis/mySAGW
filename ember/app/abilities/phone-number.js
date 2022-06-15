import BaseAbility from "mysagw/abilities/-base";

export default class PhoneNumberAbility extends BaseAbility {
  get showMultiLangDescription() {
    return this.isStaff;
  }
  canAdd() {
    return this.isStaffOrOwnIdentity(this.model);
  }

  canEdit() {
    return this.isStaffOrOwnIdentity(this.model);
  }

  canDelete() {
    return this.isStaffOrOwnIdentity(this.model);
  }
}
