import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import {
  dropTask,
  restartableTask,
  lastValue,
} from "ember-concurrency-decorators";
import UIkit from "uikit";

import applyError from "mysagw/utils/apply-error";
import PhoneValidations from "mysagw/validations/phone-number";

/**
 * @arg identity
 */
export default class IdentityPhoneNumbersComponent extends Component {
  @service notification;
  @service store;
  @service intl;

  // Lifecycle

  @action onUpdate() {
    this.fetchPhoneNumbers.perform(this.args.identity);
  }

  // List

  @lastValue("fetchPhoneNumbers") phoneNumbers;

  @restartableTask *fetchPhoneNumbers(identity) {
    return yield this.store.query("phone-number", {
      filter: { identity: identity.id },
      include: "identity",
    });
  }

  // Add / Edit

  validations = PhoneValidations;

  @tracked changeset = null;

  @action edit(phoneNumber) {
    this.changeset = Changeset(
      phoneNumber ||
        this.store.createRecord("phone-number", {
          identity: this.args.identity,
        }),
      lookupValidator(PhoneValidations),
      PhoneValidations
    );
  }

  @action cancel() {
    this.changeset = null;
  }

  @dropTask *submit(changeset) {
    try {
      // Apply changes and save.
      yield changeset.save({
        adapterOptions: { include: "identity,identity.phone-numbers" },
      });

      // Reset form and list.
      // TODO Update `phoneNumbers` via Ember Data store.
      this.onUpdate();
      this.changeset = null;
    } catch (error) {
      // A "unique" error can only apply to the phone number.
      // But as the backend validation doesn't stem from the field itself
      // it cannot automatically be attributed by `applyError`. That's why we add
      // the specific field error manually to the changeset if present.
      const unique = error.errors?.find(({ code }) => code === "unique");
      if (unique) {
        changeset.addError("phone", unique.detail);
      }

      console.error(error);
      this.notification.fromError(error);
      applyError(changeset, error);
    }
  }

  // Delete

  @dropTask *delete(phoneNumber) {
    try {
      const options = { number: phoneNumber.phone };
      yield UIkit.modal.confirm(
        this.intl.t("components.identity-phone-numbers.delete.prompt", options)
      );

      try {
        yield phoneNumber.destroyRecord();
        this.notification.success(
          this.intl.t(
            "components.identity-phone-numbers.delete.success",
            options
          )
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
