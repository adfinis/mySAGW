import BaseAbility from "mysagw/abilities/-base";

export default class AdditionalEmailAbility extends BaseAbility {
  get showMultiLangDescription() {
    return this.isStaff;
  }

  canAdd(identity) {
    return this.isStaffOrOwnIdentity(identity);
  }

  canEdit(identity) {
    return this.isStaffOrOwnIdentity(identity);
  }

  canDelete(identity) {
    return this.isStaffOrOwnIdentity(identity);
  }
}
