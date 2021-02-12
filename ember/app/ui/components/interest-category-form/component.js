import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency-decorators";
import InterestCategoryValidations from "mysagw/validations/interest-category";

/**
 * @arg category
 * @arg onSave
 */
export default class InterestCategoryFormComponent extends Component {
  @service notification;
  @service store;
  @service intl;

  @tracked model;

  validations = InterestCategoryValidations;

  @action onUpdate() {
    this.model =
      this.args.category || this.store.createRecord("interest-category");
  }

  @dropTask *submit(changeset) {
    try {
      changeset.execute();
      yield this.model.save();
      this.notification.success(
        this.intl.t("component.interest-category-form.success", {
          category: this.model.title,
        })
      );
      this.args.onSave?.(this.model);
    } catch (error) {
      console.error(error);
      this.notification.danger(error.message);
    }
  }
}
