import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

import ENV from "mysagw/config/environment";

export default class CaseStateLabelComponent extends Component {
  @tracked icons = ENV.APP.caseStateIcons;

  get iconLeft() {
    return this.args.iconPosition !== "right";
  }
}
