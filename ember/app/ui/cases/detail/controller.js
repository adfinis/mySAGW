import Controller from "@ember/controller";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { dropTask } from "ember-concurrency";

export default class CasesDetailController extends Controller {
  @calumaQuery({ query: allWorkItems })
  workItemsQuery;

  @dropTask
  *fetchWorkItems() {
    yield this.workItemsQuery.fetch({
      filter: [{ task: "circulation" }, { case: this.model.id }],
    });
  }

  get circulation() {
    return this.workItemsQuery.value.firstObject;
  }
}
