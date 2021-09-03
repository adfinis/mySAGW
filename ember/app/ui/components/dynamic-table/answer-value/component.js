import Component from "@glimmer/component";

export default class AnswerValue extends Component {
  get value() {
    const answer = this.args.value
      .mapBy("node")
      .findBy("question.slug", this.args.tdDefinition.questionSlug);

    if (answer) {
      return answer[`${answer.__typename}Value`];
    }

    return "";
  }
}
