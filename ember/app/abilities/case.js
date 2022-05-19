import BaseAbility from "mysagw/abilities/-base";

export default class CaseAbility extends BaseAbility {
  get canExportForAccounting() {
    return this.isStaff;
  }

  get canList() {
    return this.hasAccess(this.model) || this.isStaff;
  }

  get canEdit() {
    return this.hasAccess(this.model);
  }

  get canDelete() {
    return this.model.hasSubmitWorkItem || this.isStaff;
  }

  get canAddAccess() {
    return this.hasAccess(this.model) || this.isAdmin;
  }

  get canDeleteAccess() {
    return (
      ((this.access.email ||
        this.model.accesses.filter((access) => {
          return !access.email && access.caseId === this.access.caseId;
        }).length > 1) &&
        this.hasAccess(this.model)) ||
      this.isAdmin
    );
  }
}
