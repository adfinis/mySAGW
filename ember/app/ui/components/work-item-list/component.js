import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class WorkItemListComponent extends Component {
  @action
  fetchMore() {
    this.args.query.fetchMore();
  }
}
