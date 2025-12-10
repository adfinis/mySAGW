import { get } from "@ember/object";
import Component from "@glimmer/component";

import formatCurrency from "mysagw/utils/format-currency";

export default class AnswerValue extends Component {
  get value() {
    const value = this.args.value.parentWorkItem ?? this.args.value;

    const answer = get(value, this.args.tdDefinition.answerKey)
      .map((answer) => answer.node)
      .find((i) => i.question.slug === this.args.tdDefinition.questionSlug);

    if (!answer || !answer[`${answer.__typename}Value`]) {
      return "";
    }

    if (answer.question.__typename === "ChoiceQuestion") {
      return answer.question.options.edges.find(
        (option) => option.node.slug === answer[`${answer.__typename}Value`],
      ).node.label;
    }

    if (answer.question.meta?.waehrung) {
      return formatCurrency(
        answer[`${answer.__typename}Value`],
        answer.question.meta.waehrung,
      );
    }

    return answer[`${answer.__typename}Value`];
  }
}
