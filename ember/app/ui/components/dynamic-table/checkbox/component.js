import Component from "@glimmer/component";

export default class DynamicTableCheckbox extends Component {
  get checked() {
    return this.args.tdDefinition.selected.includes(this.args.value.id);
  }
}
