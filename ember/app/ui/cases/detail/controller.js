import Controller from "@ember/controller";
import QueryParams from "ember-parachute";

export default class CasesDetailController extends Controller.extend(
  new QueryParams().Mixin
) {
  get circulation() {
    return this.model.workItems.edges.findBy("node.task.slug", "circulation");
  }
}
