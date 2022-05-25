import BaseAbility from "mysagw/abilities/-base";
import ENV from "mysagw/config/environment";

export default class CaseAbility extends BaseAbility {
  get canExportForAccounting() {
    return this.isStaffOrAdmin;
  }

  get canList() {
    return this.hasAccess(this.model) || this.isStaffOrAdmin;
  }

  get canEdit() {
    return this.hasAccess(this.model);
  }

  get canDelete() {
    return this.model.hasSubmitWorkItem || this.isStaffOrAdmin;
  }

  get canRedo() {
    return (
      ENV.APP.caluma.redoableTaskSlugs.includes(
        this.model.redoWorkItem?.task.slug
      ) &&
      this.isStaffOrAdmin &&
      (this.model.canRedoWorkItem ||
        (!this.model.workItems.findBy("task.slug", "additional-data-form") &&
          this.model.sortedWorkItems[0].task.slug === "define-amount"))
    );
  }

  get canReopen() {
    return this.model.isCompleted && this.isStaffOrAdmin;
  }

  get canAddAccess() {
    return this.hasAccess(this.model) || this.isStaffOrAdmin;
  }

  get canDeleteAccess() {
    return (
      ((this.access.email ||
        this.model.accesses.filter((access) => {
          return !access.email && access.caseId === this.access.caseId;
        }).length > 1) &&
        this.hasAccess(this.model)) ||
      this.isStaffOrAdmin
    );
  }
}
