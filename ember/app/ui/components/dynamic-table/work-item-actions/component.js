import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { performHelper } from "ember-concurrency/helpers/perform";

export default class WorkItemActions extends Component {
  @service router;
  @service intl;
  @service can;

  get actions() {
    if (this.can.cannot("edit work-item")) {
      return [];
    }

    return [this.editAction, this.assignToMeAction].filter(Boolean);
  }

  get editAction() {
    return {
      action: performHelper([this.edit], {}),
      title: this.intl.t("work-items.actions.edit"),
    };
  }

  get assignToMeAction() {
    if (this.args.value.isAssignedToCurrentUser) {
      return null;
    }

    return {
      action: performHelper([this.assignToMe], {}),
      title: this.intl.t("work-items.actions.assignToMe"),
    };
  }

  @dropTask
  *assignToMe(event) {
    event.preventDefault();

    yield this.args.value.assignToMe();
  }

  @dropTask
  *edit(event) {
    event.preventDefault();

    return yield this.router.transitionTo(
      "cases.detail.work-items.edit",
      this.args.value.case.id,
      this.args.value.id,
    );
  }
}
