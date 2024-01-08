import BaseAbility from "mysagw/abilities/-base";

export default class PhoneNumberAbility extends BaseAbility {
  get showMultiLangDescription() {
    return this.isStaff;
  }

  get canAdd() {
    return this.canEditIdentity(this.model);
  }

  get canEdit() {
    return this.canEditIdentity(this.model);
  }

  get canDelete() {
    return this.canEditIdentity(this.model);
  }
}
