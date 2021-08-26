import Controller from "@ember/controller";

import ENV from "mysagw/config/environment";

export default class CasesDetailEditController extends Controller {
  get disabled() {
    return !this.model.workItems.edges
      .mapBy("node")
      .filter((workItem) =>
        ENV.APP.caluma.documentEditableTaskSlugs.includes(workItem.task.slug)
      )
      .isAny("status", "READY");
  }
}
