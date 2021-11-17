import BaseAbility from "mysagw/abilities/-base";

export default class CaseAbility extends BaseAbility {
  get canExportForAccounting() {
    return this.isStaff;
  }

  get canList() {
    return this.hasAccess(this.model) || this.isStaff;
  }

  get canAdd() {
    return this.hasAccess(this.model);
  }

  get canDelete() {
    return (
      (this.invitation.email ||
        this.model.invitations.filter((invitation) => {
          return (
            !invitation.email && invitation.caseId === this.invitation.caseId
          );
        }).length > 1) &&
      this.hasAccess(this.model)
    );
  }
}
