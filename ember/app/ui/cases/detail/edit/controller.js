import Controller from "@ember/controller";
import ENV from "mysagw/config/environment";

export default class CasesDetailEditController extends Controller {
  get disabled() {
    return !this.model.workItems.edges
      .mapBy("node")
      .find(
        (workItem) =>
          (workItem.task.slug === ENV.APP.caluma.submitTaskSlug ||
            workItem.task.slug === ENV.APP.caluma.reviseTaskSlug) &&
          workItem.status === "READY"
      );
  }
}
