import { get } from "@ember/object";
import Component from "@glimmer/component";

export default class AnswerValue extends Component {
  get value() {
    const value = this.args.value.parentWorkItem ?? this.args.value;

    const answer = get(value, this.args.tdDefinition.answerKey)
      .mapBy("node")
      .findBy("question.slug", this.args.tdDefinition.questionSlug);

    if (answer) {
      return answer[`${answer.__typename}Value`];
    }

    return "";
  }
}
