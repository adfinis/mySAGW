import Component from "@glimmer/component";

export default class AnswerValue extends Component {
  get value() {
    const caseObj = this.args.value?.case ?? this.args.value;
    let answers = caseObj.document.answers?.edges;

    if (caseObj.parentWorkItem) {
      answers = caseObj.parentWorkItem.case.document.answers.edges;
    }

    const answer = answers
      .mapBy("node")
      .findBy("question.slug", this.args.tdDefinition.questionSlug);

    if (answer) {
      return answer[`${answer.__typename}Value`];
    }

    return "";
  }
}
