import Component from "@glimmer/component";
import moment from "moment";

export default class TaskName extends Component {
  get highlightClasses() {
    const diff = this.args.value.deadline?.diff(moment(), "days", true);

    return [
      "highlight",
      ...(diff <= 0 ? ["highlight--expired"] : []),
      ...(diff <= 3 && diff > 0 ? ["highlight--expiring"] : []),
    ].join(" ");
  }
}
