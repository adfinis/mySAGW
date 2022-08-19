import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class FiltersDropdownComponent extends Component {
  @tracked selection = this.args.selected;

  @action
  setSelection(value) {
    this.selection = value;
    this.args.onChange(value);
  }
}
