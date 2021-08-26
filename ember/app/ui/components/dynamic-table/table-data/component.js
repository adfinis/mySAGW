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

  get showAccent() {
    if (
      this.args.value.status === "RUNNING" &&
      this.args.tdDefinition.firstItem
    ) {
      return "accent-border-left";
    }

    return "";
  }
}
