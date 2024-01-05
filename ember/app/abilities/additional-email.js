import BaseAbility from "mysagw/abilities/-base";

export default class AdditionalEmailAbility extends BaseAbility {
  get showMultiLangDescription() {
    return this.isStaff;
  }

  canAdd() {
    return this.canEditIdentity(this.model);
  }

  canEdit() {
    return this.canEditIdentity(this.model);
  }

  canDelete() {
    return this.canEditIdentity(this.model);
  }
}
