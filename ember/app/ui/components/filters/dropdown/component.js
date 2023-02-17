import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import {
  arrayFromString,
} from "mysagw/utils/query-params";
export default class FiltersDropdownComponent extends Component {
  @tracked selection = this.selected;

  get selected() {
    console.log(this.args.selected);
    const selected = arrayFromString(this.args.selected ?? "");

    return (
      this.args.options?.filter((option) => selected.includes(option.value)) ??
      []
    );
  }

  @action
  setSelection(value) {
    this.selection = value;
    this.args.onChange(value);
  }
}
