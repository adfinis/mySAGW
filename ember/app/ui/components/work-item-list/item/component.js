import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { performHelper } from "ember-concurrency/helpers/perform";
import moment from "moment";

export default class WorkItemListItemComponent extends Component {
  @service router;
  @service intl;
  @service can;
  @service store;

  get actions() {
    if (this.can.cannot("edit work-item")) {
      return [];
    }

    return [this.editAction, this.assignToMeAction].filter(Boolean);
  }

  get editAction() {
    return {
      action: performHelper([this.edit], {}),
      title: this.intl.t("workItems.actions.edit"),
    };
  }

  get assignToMeAction() {
    if (this.args.workItem.isAssignedToCurrentUser) {
      return null;
    }

    return {
      action: performHelper([this.assignToMe], {}),
      title: this.intl.t("workItems.actions.assignToMe"),
    };
  }

  get highlightClasses() {
    if (!this.args.highlight) {
      return "";
    }

    const diff = this.args.workItem.deadline?.diff(moment(), "days", true);

    return [
      "highlight",
      ...(diff <= 0 ? ["highlight--expired"] : []),
      ...(diff <= 3 && diff > 0 ? ["highlight--expiring"] : []),
    ].join(" ");
  }

  @dropTask
  *assignToMe(event) {
    event.preventDefault();

    yield this.args.workItem.assignToMe();
  }

  @dropTask
  *edit(event) {
    event.preventDefault();

    return yield this.router.transitionTo(
      "cases.detail.work-items.edit",
      this.args.workItem.case.id,
      this.args.workItem.id
    );
  }

  @dropTask
  *getIdentity() {
    if (this.can.cannot("edit work-item")) {
      return;
    }

    let idpId = null;

    if (
      !this.args.workItem.assignedUser &&
      this.args.workItem.assignedUsers[0]
    ) {
      idpId = this.args.workItem.assignedUsers[0];
    }

    if (this.args.workItem.isCompleted && !this.args.workItem.closedByUser) {
      idpId = this.args.workItem.raw.closedByUser;
    }

    if (idpId) {
      return yield this.store.query("identity", {
        filter: { idpId },
      });
    }
  }
}
