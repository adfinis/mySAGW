import { action } from "@ember/object";
import Component from "@glimmer/component";

const invert = /^-/;

export default class DynamicTableHeaderComponent extends Component {
  get isActive() {
    return this.args.order.replace(invert, "") === this.args.config.sortKey;
  }

  get icon() {
    return invert.test(this.args.order) ? "triangle-down" : "triangle-up";
  }

  @action
  order() {
    const direction = this.isActive && !invert.test(this.args.order) ? "-" : "";
    const order = `${direction}${this.args.config.sortKey}`;

    this.args.setOrder(order);
  }
}
