import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency-decorators";

import applyError from "mysagw/utils/apply-error";
import InterestCategoryValidations from "mysagw/validations/interest-category";

/**
 * @arg category
 * @arg onSave
 */
export default class InterestCategoryFormComponent extends Component {
  @service notification;
  @service store;
  @service intl;
  @service router;

  @tracked model;
  @tracked validations = InterestCategoryValidations;
  @tracked backToInterests;

  @action
  onUpdate() {
    this.model =
      this.args.category || this.store.createRecord("interest-category");
  }

  @action
  setBackToInterests() {
    this.backToInterests = true;
  }

  @dropTask
  *submit(changeset) {
    try {
      yield changeset.save();
      this.notification.success(
        this.intl.t("components.interest-category-form.success", {
          category: this.model.title,
        })
      );

      this.args.onSave?.(this.model);

      if (this.backToInterests) {
        this.router.transitionTo("interests");
      }
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
      applyError(changeset, error);
    }
  }
}
