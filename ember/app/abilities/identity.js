import BaseAbility from "mysagw/abilities/-base";

export default class IdentityAbility extends BaseAbility {
  get canList() {
    return this.isStaff;
  }

  get canAdd() {
    return this.isStaff;
  }

  get canEdit() {
    return this.canEditIdentity(this.model);
  }

  get canDelete() {
    return this.isStaff;
  }

  get canEditOrganisation() {
    return this.isStaff;
  }

  get canAddInterest() {
    return this.canEditIdentity(this.model);
  }

  get canRemoveInterest() {
    return this.canEditIdentity(this.model);
  }
}
