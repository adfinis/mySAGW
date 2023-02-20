import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import Changeset from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask } from "ember-concurrency";

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

  @tracked changeset;
  @tracked backToInterests;

  @action
  onUpdate() {
    this.changeset = new Changeset(
      this.args.category || this.store.createRecord("interest-category"),
      lookupValidator(InterestCategoryValidations),
      InterestCategoryValidations
    );
  }

  @action
  setBackToInterests(event) {
    event.preventDefault();
    this.backToInterests = true;
    this.submit.perform(this.changeset);
  }

  @dropTask
  *submit(changeset) {
    try {
      yield changeset.save();
      this.notification.success(
        this.intl.t("components.interest-category-form.success", {
          category: changeset.title,
        })
      );

      this.args.onSave?.(this.changeset);

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
