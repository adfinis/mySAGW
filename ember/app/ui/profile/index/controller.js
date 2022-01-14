import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { restartableTask } from "ember-concurrency";
import QueryParams from "ember-parachute";

const queryParams = new QueryParams({
  // Convert the tab number to a string so its human readable
  activeTab: {
    defaultValue: "identity",
    serialize(value) {
      return value ? "memberships" : "identity";
    },
    deserialize(value) {
      return value === "identity" ? 0 : 1;
    },
  },
});

export default class ProfileIndexController extends Controller.extend(
  queryParams.Mixin
) {
  @service store;
  @service notification;

  @tracked activeTab = 0;
  @tracked pageSize = 10;
  @tracked pageNumber = 1;
  @tracked totalPages = 1;
  @tracked memberships = [];

  get hasNextPage() {
    return this.pageNumber < this.totalPages;
  }

  @restartableTask
  *fetchMemberships() {
    try {
      const memberships = yield this.store.query(
        "membership",
        {
          include: "organisation,role",
          page: {
            number: this.pageNumber,
            size: this.pageSize,
          },
        },
        { adapterOptions: { customEndpoint: "my-memberships" } }
      );

      this.totalPages = memberships.meta.pagination?.pages;
      this.memberships = [...this.memberships, ...memberships.toArray()];

      return memberships;
    } catch (error) {
      console.error(error);

      this.notification.fromError(error);
    }
  }

  @action
  loadMoreMemberships() {
    this.pageNumber += 1;
    this.fetchMemberships.perform();
  }

  @action
  setActiveTab(tab) {
    this.activeTab = tab;
  }
}
