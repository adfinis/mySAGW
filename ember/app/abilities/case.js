import BaseAbility from "mysagw/abilities/-base";
import ENV from "mysagw/config/environment";

export default class CaseAbility extends BaseAbility {
  get canExportForAccounting() {
    return this.isStaffOrAdmin;
  }

  get canList() {
    return this.canListUser || this.canListAdmin;
  }

  get canListAdmin() {
    return this.isStaffOrAdmin;
  }

  get canListUser() {
    return this.hasAccess(this.model);
  }

  get canEdit() {
    return (
      this.isAdmin ||
      (this.model.hasSubmitOrReviseWorkItem && this.hasAccess(this.model))
    );
  }

  get canDelete() {
    return this.model.hasSubmitOrReviseWorkItem || this.isStaffOrAdmin;
  }

  get canRedo() {
    /*
     * Only when additional-data-form isnt present can define-amount be redone,
     * as it means the additional-data step was skipped.
     * Otherwise canRedoWorkItem returns the work item which can be redone.
     */
    return (
      ENV.APP.caluma.redoableTaskSlugs.includes(
        this.model.redoWorkItem?.task.slug,
      ) &&
      this.isStaffOrAdmin &&
      (this.model.canRedoWorkItem ||
        (!this.model.workItems.findBy("task.slug", "additional-data-form") &&
          this.model.workItems[0].task.slug === "define-amount"))
    );
  }

  get canReopen() {
    return this.model.isCompleted && this.isStaffOrAdmin;
  }

  get canCreateHiddenForm() {
    return this.isStaffOrAdmin;
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

  get canFilterAccess() {
    return this.isStaffOrAdmin;
  }

  get canFilterAllForms() {
    return this.isStaffOrAdmin;
  }
}
