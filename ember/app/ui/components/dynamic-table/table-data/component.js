import { get } from "@ember/object";
import Component from "@glimmer/component";

export default class DynamicTableTableDataComponent extends Component {
  get componentName() {
    return `dynamic-table/${this.args.tdDefinition.type || "text"}`;
  }

  get value() {
    return get(this.args.value, this.args.tdDefinition.modelKey);
  }

  get linkToModel() {
    return get(
      this.args.value,
      this.args.tdDefinition.linkToModelField || "id"
    );
  }

  get hasRunningWorkItem() {
    return this.args.value.workItems.edges
      .mapBy("node")
      .some((workItem) => workItem.status === "READY");
  }
}
