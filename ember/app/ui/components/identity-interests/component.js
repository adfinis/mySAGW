import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask, restartableTask, lastValue } from "ember-concurrency";
import applyError from "mysagw/utils/apply-error";
import InterestValidations from "mysagw/validations/identity-interest";
import UIkit from "uikit";

/**
 * @arg identity
 */
export default class IdentityInterestsComponent extends Component {
  @service store;
  @service intl;
  @service notification;

  @tracked categories;

  // Lifecycle

  @action onUpdate() {
    this.categories = this.parseOwnInterests(this.args.identity);
    this.fetchInterestCategories.perform();
  }

  // List

  parseOwnInterests(identity) {
    return identity.interests
      .getEach("category")
      .uniqBy("id")
      .map((category) => ({
        title: category.get("title"),
        interests: identity.interests.filterBy(
          "category.id",
          category.get("id")
        ),
      }));
  }

  // Add / Edit

  @tracked changeset = null;

  @action edit(interest) {
    this.changeset = Changeset(
      { interest },
      lookupValidator(InterestValidations),
      InterestValidations
    );
  }

  @action cancel() {
    this.changeset = null;
  }

  @dropTask *submit(changeset) {
    try {
      // Apply changes and save.
      changeset.execute();
      this.args.identity.interests.pushObject(changeset.interest);
      yield this.args.identity.save();

      // Reset form and list.
      // TODO Update `categories` via Ember Data store.
      this.onUpdate();
      this.changeset = null;
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
      applyError(changeset, error);
    }
  }

  @lastValue("fetchInterestCategories") interestCategories;

  @restartableTask *fetchInterestCategories() {
    const interests = yield this.store.findAll("interest", {
      include: "category",
    });

    return interests
      .getEach("category")
      .uniqBy("id")
      .map((category) => ({
        groupName: category.get("title"),
        options: interests.filterBy("category.id", category.get("id")),
      }));
  }

  // Delete

  @dropTask *delete(interest) {
    try {
      const options = { interest: interest.title };
      yield UIkit.modal.confirm(
        this.intl.t("component.identity-interests.delete.prompt", options)
      );

      try {
        this.args.identity.interests.removeObject(interest);
        this.args.identity.save();

        this.notification.success(
          this.intl.t("component.identity-interests.delete.success", options)
        );
        // Reset list.
        // TODO Update `categories` via Ember Data store.
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
