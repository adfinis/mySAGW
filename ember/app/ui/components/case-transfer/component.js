import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class CaseTransfer extends Component {
  @service store;
  @service notification;
  @service intl;
  @service fetch;

  @tracked transferModalVisible = false;
  @tracked removeAccess = false;
  @tracked newAssignees = [];

  @action
  selectNewAssignees(value) {
    this.newAssignees = value.map((assignee) => assignee.id);
  }

  @action
  async transferCases() {
    const adapter = this.store.adapterFor("case-access");
    const uri = `${adapter.buildURL("case-access")}/transfer`;

    const caseIds = [];
    const dossierNrs = [];
    this.args.cases.forEach((c) => {
      caseIds.push(c.id);
      dossierNrs.push(c.documentNumber);
    });

    const body = {
      case_ids: caseIds,
      dossier_nrs: dossierNrs,
      new_assignees: this.newAssignees,
      to_remove_assignees: [],
    };

    if (this.removeAccess) {
      body.to_remove_assignees = this.args.toRemove;
    }

    const headers = adapter.headers;
    headers["content-type"] = "application/json";

    try {
      await this.fetch.fetch(uri, {
        method: "POST",
        headers,
        body: JSON.stringify(body),
      });

      this.notification.success(
        this.intl.t("documents.bulkEdit.transfer.success"),
      );

      this.transferModalVisible = false;
      this.removeAccess = false;
      this.newAssignees = [];

      await this.args.afterTransfer();
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }
}
