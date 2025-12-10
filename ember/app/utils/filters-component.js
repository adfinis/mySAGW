import { service } from "@ember/service";
import Component from "@glimmer/component";
import { trackedFunction } from "reactiveweb/function";

import ENV from "mysagw/config/environment";
import getOptionsQuery from "mysagw/gql/queries/get-options.graphql";

export default class FiltersComponent extends Component {
  @service apollo;
  @service filteredForms;

  forms = trackedFunction(this, async () => {
    await Promise.resolve();

    const forms = await this.filteredForms.fetch();

    return forms.map((node) => ({
      value: node.slug,
      label: node.name,
    }));
  });

  questionOptions = trackedFunction(this, async () => {
    const response = await this.apollo.query(
      {
        query: getOptionsQuery,
        variables: {
          filter: [
            { slugs: Object.values(ENV.APP.caluma.filterableQuestions) },
          ],
          order: [{ attribute: "NAME" }],
        },
      },
      "allQuestions.edges",
    );

    return response.map((option) => option.node);
  });

  getFormattedOptions(slug) {
    if (!this.questionOptions.value) {
      return [];
    }

    const question = this.questionOptions.value.filter(
      (value) => value.slug === slug,
    )[0];

    if (!question) {
      return [];
    }

    const options = question[question.__typename].edges;

    return options.map((edge) => ({
      value: edge.node.slug,
      label: edge.node.label,
    }));
  }

  get expertAssociations() {
    return this.getFormattedOptions(
      ENV.APP.caluma.filterableQuestions.expertAssociations,
    );
  }

  get distributionPlans() {
    return this.getFormattedOptions(
      ENV.APP.caluma.filterableQuestions.distributionPlans,
    );
  }

  get sections() {
    return this.getFormattedOptions(
      ENV.APP.caluma.filterableQuestions.sections,
    );
  }

  get setFiltersAmount() {
    return Object.values(this.args.filters).reduce((total, value) => {
      if (new Set(["open", "all"]).has(value) || !value) {
        return total;
      }

      return total + 1;
    }, 0);
  }
}
