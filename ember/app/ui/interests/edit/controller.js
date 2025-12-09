import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask } from "ember-concurrency";
import UIkit from "uikit";

import InterestValidations from "mysagw/validations/interest";

export default class InterestsEditController extends Controller {
  @service notification;
  @service store;
  @service intl;

  @tracked changeset = null;

  get interests() {
    return this.model.interests.filterBy("isNew", false);
  }

  @action
  edit(interest) {
    this.changeset = Changeset(
      interest ||
        this.store.createRecord("interest", {
          category: this.model,
        }),
      lookupValidator(InterestValidations),
      InterestValidations,
    );
  }

  @action
  cancel() {
    this.changeset = null;
  }

  @dropTask
  *submit(changeset) {
    try {
      // Apply changes and save.
      yield changeset.save();

      // Reset form and list.
      this.changeset = null;
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  // Delete

  @dropTask
  *delete(interest) {
    try {
      const options = { interest: interest.title };
      yield UIkit.modal.confirm(
        this.intl.t("interests.edit.delete.prompt", options),
      );

      try {
        yield interest.destroyRecord();
        this.notification.success(
          this.intl.t("interests.edit.delete.success", options),
        );
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
