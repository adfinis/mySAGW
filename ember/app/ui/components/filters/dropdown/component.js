import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class DropdownComponent extends Component {
  @tracked selection = [];

  @action
  setSelection(value) {
    this.selection = value;
    this.args.onChange(value);
  }
}
