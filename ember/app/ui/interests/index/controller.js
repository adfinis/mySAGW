import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { dropTask, restartableTask, lastValue } from "ember-concurrency";
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
  get categories() {
    return this.allCategories?.filterBy("isNew", false);
  }

  @lastValue("fetchInterests") allCategories;

  @restartableTask *fetchInterests() {
    try {
      return yield this.store.findAll("interest-category", {
        include: "interests",
      });
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @dropTask *delete(category) {
    try {
      const options = { category: category.title };
      yield UIkit.modal.confirm(
        this.intl.t("interests.index.delete.prompt", options),
      );

      try {
        yield category.destroyRecord();
        this.notification.success(
          this.intl.t("interests.index.delete.success", options),
        );
        this.onUpdate();
      } catch (error) {
        console.error(error);
        this.notification.fromError(error);
      }
    } catch (error) {
      // Dialog was dimissed. No action necessary.
      // Log the error anyway in case something else broke in the try.
      console.error(error);
    }
  }
}
