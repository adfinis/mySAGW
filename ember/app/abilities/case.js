import BaseAbility from "mysagw/abilities/-base";

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

  get canBulkEdit() {
    return this.isAdmin;
  }

  get canDelete() {
    return this.model.hasSubmitOrReviseWorkItem || this.isStaffOrAdmin;
  }

  get canRedo() {
    const canRedoTaskSlug = [
      "circulation",
      "decision-and-credit",
      "additional-data",
      "complete-document",
    ];

    // Only when additional-data-form isnt present can define-amount be redone,
    // as it means the additional-data step was skipped.
    // This is handled in the backend by the dynamic task redo-define-amount.
    const additionalDataFormWorkItem = this.model.workItems.find(
      (wi) => wi.task.slug === "additional-data-form",
    );
    const defineAmountWorkItem = this.model.readyWorkItems.find(
      (wi) => wi.task.slug === "define-amount",
    );
    if (!additionalDataFormWorkItem && defineAmountWorkItem) {
      canRedoTaskSlug.push("define-amount");
    }

    const canRedo = this.model.readyWorkItems.some((workItem) =>
      canRedoTaskSlug.includes(workItem.task.slug),
    );

    return this.isStaffOrAdmin && canRedo;
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
