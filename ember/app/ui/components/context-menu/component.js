import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { runTask, cancelTask } from "ember-lifeline";

export default class ContextMenuComponent extends Component {
  @tracked menuOpen = false;
  closeMenuDelay;

  @action
  handleMouseLeave() {
    this.closeMenuDelay = runTask(
      this,
      function () {
        this.menuOpen = false;
      },
      1000,
    );
  }

  @action
  handleMouseEnter() {
    cancelTask(this, this.closeMenuDelay);
  }
}
