import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency-decorators";

export default class CaseAccessActionsComponent extends Component {
  @service router;
  @service can;

  @dropTask
  *deleteRow(access) {
    yield this.args.tdDefinition.additionalInfo.accesses
      .find((a) => {
        return (
          a.identity.get("id") === access.identity.get("id") ||
          (a.email === access.email && access.email !== null)
        );
      })
      .destroyRecord();

    if (this.can.cannot("list case", this.args.tdDefinition.additionalInfo)) {
      this.router.transitionTo("cases");
    }
  }
}
