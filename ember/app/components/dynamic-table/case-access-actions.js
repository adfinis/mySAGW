import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

export default class CaseAccessActionsComponent extends Component {
  @service router;
  @service can;

  @dropTask
  *deleteRow(access) {
    yield this.args.tdDefinition.additionalInfo.accesses
      .find((a) => {
        return (
          (access.identity &&
            a.identity?.get("id") === access.identity.get("id")) ||
          (a.email === access.email && !access.identity)
        );
      })
      .destroyRecord();

    if (this.can.cannot("list case", this.args.tdDefinition.additionalInfo)) {
      this.router.transitionTo("cases");
    }
  }
}
