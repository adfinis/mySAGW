import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask, restartableTask, lastValue } from "ember-concurrency";
import UIkit from "uikit";

import applyError from "mysagw/utils/apply-error";
import InterestValidations from "mysagw/validations/identity-interest";

/**
 * @arg identity
 */
export default class IdentityInterestsComponent extends Component {
  @service store;
  @service intl;
  @service notification;

  @tracked categories;

  // Lifecycle

  @action
  onUpdate() {
    this.fetchInterestCategories.perform();
  }

  // List

  async parseOwnInterests(identity) {
    return (await identity.interests)
      .map((interest) => interest.category)
      .uniqBy("id")
      .map(async (category) => ({
        title: category.get("title"),
        interests: (await identity.interests).filter(
          (interest) => interest.category.get("id") === category.get("id"),
        ),
      }));
  }

  @action
  openPowerSelect(select) {
    select.actions.open();
  }

  // Add / Edit

  @tracked changeset = null;

  @action
  edit(interest) {
    this.changeset = Changeset(
      { interest },
      lookupValidator(InterestValidations),
      InterestValidations,
    );
  }

  @action
  cancel() {
    this.changeset = null;
  }

  get endpoint() {
    if (this.args.endpoint) {
      return {
        adapterOptions: { customEndpoint: this.args.endpoint },
      };
    }
    return {};
  }

  @dropTask
  *submit(changeset) {
    try {
      // Apply changes and save.
      changeset.execute();
      this.args.identity.interests.pushObject(changeset.interest);
      yield this.args.identity.save(this.endpoint);

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
  @restartableTask
  *fetchInterestCategories() {
    const interests = yield this.store.query("interest", {
      filter: { public: this.args.profileView },
      include: "category",
    });

    this.categories = yield this.parseOwnInterests(this.args.identity);

    return interests
      .map((interest) => interest.category)
      .uniqBy("id")
      .map((category) => ({
        groupName: category.get("title"),
        options: interests.filter(
          (interest) => interest.category.get("id") === category.get("id"),
        ),
      }));
  }

  // Delete

  @dropTask
  *delete(interest) {
    try {
      const options = { interest: interest.title };
      yield UIkit.modal.confirm(
        this.intl.t("components.identity-interests.delete.prompt", options),
      );

      try {
        this.args.identity.interests.removeObject(interest);
        this.args.identity.save(this.endpoint);

        this.notification.success(
          this.intl.t("components.identity-interests.delete.success", options),
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
