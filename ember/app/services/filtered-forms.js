import Service, { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";

import getFilteredFormsQuery from "mysagw/gql/queries/get-filtered-forms.graphql";
import getFormsQuery from "mysagw/gql/queries/get-forms.graphql";

export default class FilteredFormsService extends Service {
  @service store;

  @queryManager apollo;

  @tracked value = null;

  async fetch() {
    if (this.value !== null) return this.value;

    const organisations = (
      await this.store.findAll("identity", {
        reload: true,
        adapterOptions: { customEndpoint: "my-orgs" },
      })
    ).filterBy("isAuthorized");

    const isExpertAssociation = organisations.isAny("isExpertAssociation");
    const isAdvisoryBoard = organisations.isAny("isAdvisoryBoard");

    // todo more generic filtering
    // this is abyssmal
    const allForms = {
      ...(await this.apollo.query({
        query: getFilteredFormsQuery,
      })),
    };

    if (!isExpertAssociation) {
      delete allForms.expertAssociation;
    }
    if (!isAdvisoryBoard) {
      delete allForms.advisoryBoard;
    }
    if (!isExpertAssociation && !isAdvisoryBoard) {
      delete allForms.bothTypes;
    }

    const value = [
      allForms?.expertAssociation,
      allForms?.advisoryBoard,
      allForms?.bothTypes,
      allForms?.public,
    ]
      .map((forms) => {
        return forms?.edges.map((edge) => edge.node) ?? [];
      })
      .flat();

    this.value = value;

    return value;
  }

  async mainFormSlugs() {
    return (await this.mainForms()).map((form) => form.slug);
  }

  async mainForms() {
    return (
      await this.apollo.query({ query: getFormsQuery }, "allForms.edges")
    ).map((form) => form.node);
  }
}
