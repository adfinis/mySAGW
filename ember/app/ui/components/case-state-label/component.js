import Component from "@glimmer/component";

import ENV from "mysagw/config/environment";

export default class CaseStateLabelComponent extends Component {
  icons = ENV.APP.caseStateIcons;

  get iconLeft() {
    return !(this.args.iconPosition === "right");
  }
}
