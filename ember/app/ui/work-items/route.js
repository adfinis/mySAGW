import { service } from "@ember/service";

import TableRoute from "mysagw/utils/table-route";

export default class WorkItemsIndexRoute extends TableRoute {
  @service router;
  @service can;

  beforeModel() {
    if (this.can.cannot("list work-item")) {
      return this.router.transitionTo("index");
    }
  }
}
