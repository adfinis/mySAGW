import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class WorkItemListComponent extends Component {
  @action
  async fetchMore() {
    await this.args.query.fetchMore();
    if (typeof this.args.fetchMoreSupplement === "function") {
      await this.args.fetchMoreSupplement();
    }
  }
}
