import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";
import {
  lastValue,
  enqueueTask,
  restartableTask,
  timeout,
} from "ember-concurrency";
import { TrackedObject } from "tracked-built-ins";

import { stringFromArray } from "mysagw/utils/query-params";

export default class TableController extends Controller {
  queryParams = ["order", "filter"];

  // Filters
  _filters = {
    documentNumber: "",
    identities: "",
    answerSearch: "",
    forms: "",
    expertAssociations: "",
    distributionPlan: "",
    sections: "",
  };
  @tracked filters = new TrackedObject(this._filters);
  @tracked invertedFilters = new TrackedObject(this._filters);
  @tracked order = "-CREATED_AT";
  @tracked filter;

  serializeFilter() {
    this.filter = btoa(
      JSON.stringify({ filters: this.filters, inverts: this.invertedFilters })
    );
  }
  @action
  deserializeFilter() {
    if (!this.filter) {
      return;
    }

    const { filters, inverts } = JSON.parse(atob(this.filter));
    this.filters = new TrackedObject(filters);
    this.invertedFilters = new TrackedObject(inverts);
  }

  @restartableTask
  *updateFilter(type, eventOrValue) {
    if (["documentNumber", "answerSearch"].includes(type)) {
      // debounce only input filters by 500ms to prevent too many requests when
      // typing into a search field
      yield timeout(500);
    }

    // Update the filter with the passed value. This can either be an array of
    // objects (multiple choice filters), and event or a plain value
    if (Array.isArray(eventOrValue)) {
      this.filters[type] = stringFromArray(
        eventOrValue,
        type === "identities" ? "idpId" : "value"
      );
    } else {
      this.filters[type] = eventOrValue.target?.value ?? eventOrValue;
    }

    this.serializeFilter();
  }

  @enqueueTask
  *invertFilter(type) {
    this.invertedFilters[type] = !this.invertedFilters[type];
    this.serializeFilter();
    yield timeout(300);
  }

  @action
  resetFilters() {
    this.filters = new TrackedObject(this._filters);
    this.invertedFilters = new TrackedObject(this._filters);
    this.serializeFilter();
  }

  @lastValue("fetchForms") forms;
  @restartableTask
  *fetchForms() {
    return yield this.filteredForms.mainFormSlugs();
  }
}
