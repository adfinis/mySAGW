import Service, { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";

import ENV from "mysagw/config/environment";
import getFormsQuery from "mysagw/gql/queries/get-forms.graphql";

export default class FilteredFormsService extends Service {
  @service store;
  @service abilities;

  @queryManager apollo;

  @tracked value = null;
  @tracked previousQuery = null;

  async fetch(queryVariables = {}) {
    if (
      this.value !== null &&
      JSON.stringify(queryVariables) === JSON.stringify(this.previousQuery)
    ) {
      return this.value;
    }

    this.value = await this.mainForms(queryVariables);
    this.previousQuery = queryVariables;

    if (this.abilities.can("filter all forms case")) {
      return this.value;
    }

    const organisations = (
      await this.store.findAll("identity", {
        reload: true,
        adapterOptions: { customEndpoint: "my-orgs" },
      })
    ).filterBy("isAuthorized");

    // map all visibilities from ENV.APP.caluma.formVisibilities
    const userVisibilities = {
      hiddenForm: this.abilities.can("create hidden form case"),
      advisoryBoardForm: organisations.isAny("isAdvisoryBoard"),
      expertAssociationForm: organisations.isAny("isExpertAssociation"),
    };

    this.value = this.value.filter((form) => {
      const visibilities = ENV.APP.caluma.formVisibilities.map(
        (visibility) => form.meta[visibility] && userVisibilities[visibility],
      );
      const publicVisibility = visibilities.every(
        (visibility) => visibility === undefined,
      );

      return publicVisibility || visibilities.any((visibility) => visibility);
    });

    return this.value;
  }

  async mainForms(variables) {
    return (
      await this.apollo.query(
        {
          query: getFormsQuery,
          variables,
        },
        "allForms.edges",
      )
    ).map((form) => form.node);
  }
}
