import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { restartableTask } from "ember-concurrency-decorators";

export default class WorkItemsIndexController extends Controller {
  queryParams = ["order", "responsible", "type", "status", "role"];

  @queryManager apollo;

  @calumaQuery({ query: allWorkItems, options: "options" })
  workItemsQuery;

  // Filters
  @tracked order = "urgent";
  @tracked responsible = "all";
  @tracked type = "all";
  @tracked status = "open";
  @tracked role = "active";

  get options() {
    return {
      pageSize: 20,
    };
  }

  get columns() {
    return [
      "task",
      "instance",
      "description",
      ...(this.status === "open"
        ? ["deadline", "responsible"]
        : ["closedAt", "closedBy"]),
    ];
  }

  @restartableTask
  *fetchWorkItems() {
    const filter = [];

    if (this.responsible === "own") {
      // TODO user
      filter.push({ assignedUsers: [] });
    } else {
      filter.push({ assignedUsers: [] });
    }

    if (this.type === "unread") {
      filter.push({ metaValue: [{ key: "not-viewed", value: true }] });
    }

    if (this.status === "closed") {
      filter.push({ status: "COMPLETED" });
    } else {
      filter.push({ status: "READY" });
    }

    if (this.role === "control") {
      // TODO group
      filter.push({ controllingGroups: [] });
    } else {
      filter.push({ addressedGroups: [] });
    }

    const order =
      this.order === "urgent"
        ? [{ attribute: "DEADLINE", direction: "ASC" }]
        : [{ attribute: "CREATED_AT", direction: "DESC" }];

    yield this.workItemsQuery.fetch({ filter, order });
  }

  @action
  updateFilter(type, value) {
    set(this, type, value);
    this.fetchWorkItems.perform();
  }
}
