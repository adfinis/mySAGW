import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

import ENV from "mysagw/config/environment";

export default class DynamicTable extends Component {
  @tracked order = {};

  get sortIcon() {
    if (this.order.direction === "ASC") {
      return "triangle-up";
    }

    return "triangle-down";
  }

  get orderKey() {
    return this.order.attribute ?? this.order.documentAnswer;
  }

  swapDirection(order) {
    if (order.direction === "ASC") {
      return "DESC";
    }

    return "ASC";
  }

  @action
  updateOrder(key) {
    // Reset direction for new key
    if (!Object.values(this.order).includes(key)) {
      this.order = {};
    }

    this.order = {
      direction: this.swapDirection(this.order),
    };

    if (ENV.APP.caluma.orderTypeKeys.attribute.includes(key)) {
      this.order.attribute = key;
    } else {
      this.order.documentAnswer = key;
    }

    this.args.setOrder(this.order);
  }
}
