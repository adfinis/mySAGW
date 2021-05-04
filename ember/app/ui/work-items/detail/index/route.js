import Route from "@ember/routing/route";

export default class WorkItemsDetailIndexRoute extends Route {
  model({ id }) {
    return id;
  }
}
