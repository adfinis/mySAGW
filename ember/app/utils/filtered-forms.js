import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { lastValue, restartableTask } from "ember-concurrency";
import { Resource } from "ember-resources";

import getFormsQuery from "mysagw/gql/queries/get-form.graphql";

export class FilteredForms extends Resource {
  @queryManager apollo;
  @service store;

  modify() {
    this.fetch.perform();
  }

  get value() {
    // sort forms, so that the ones without permissions are at the bottom
    return [
      this.allForms?.expertAssociation,
      this.allForms?.advisoryBoard,
      this.allForms?.bothTypes,
      this.allForms?.public,
    ]
      .map((forms) => {
        return forms?.edges ?? [];
      })
      .flat();
  }

  @lastValue("fetch") allForms;
  @restartableTask
  *fetch() {
    const organisations = (yield this.store.findAll("identity", {
      reload: true,
      adapterOptions: { customEndpoint: "my-orgs" },
    })).filterBy("isAuthorized");

    const isExpertAssociation = organisations.isAny("isExpertAssociation");
    const isAdvisoryBoard = organisations.isAny("isAdvisoryBoard");

    const allForms = {
      ...(yield this.apollo.query({
        query: getFormsQuery,
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

    return allForms;
  }
}
