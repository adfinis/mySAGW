import Controller from "@ember/controller";
import { action } from "@ember/object";
import { filterBy } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import {
  dropTask,
  restartableTask,
  lastValue,
} from "ember-concurrency-decorators";
import UIkit from "uikit";

export default class InterestsIndexController extends Controller {
  @service notification;
  @service store;
  @service intl;

  // Lifecycle

  @action onUpdate() {
    this.fetchInterests.perform();
  }

  // List

  @filterBy("allCategories", "isNew", false) categories;

  @lastValue("fetchInterests") allCategories;

  @restartableTask *fetchInterests() {
    try {
      return yield this.store.findAll("interest-category", {
        include: "interests",
      });
    } catch (error) {
      console.error(error);
      this.notification.danger(error.message);
    }
  }

  @dropTask *delete(category) {
    try {
      const options = { category: category.title };
      yield UIkit.modal.confirm(
        this.intl.t("page.interests.index.delete.prompt", options)
      );

      try {
        yield category.destroyRecord();
        this.notification.success(
          this.intl.t("page.interests.index.delete.success", options)
        );
        this.onUpdate();
      } catch (error) {
        console.error(error);
        this.notification.danger(error.message);
      }
    } catch (error) {
      // Dialog was dimissed. No action necessary.
    }
  }
}
