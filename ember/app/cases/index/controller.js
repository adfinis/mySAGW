import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";

export default class CasesIndexController extends Controller {
  queryParams = ["order"];
  @tracked order;

  @action
  updateOrder(event) {
    this.order = event.target.value;
  }
}
