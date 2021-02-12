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
import PhoneValidations from "mysagw/validations/phone-number";
import UIkit from "uikit";

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
      console.error(error);
      this.notification.danger(error.message);
    }
  }

  // Delete

  @dropTask *delete(phoneNumber) {
    try {
      const options = { address: phoneNumber.phone };
      yield UIkit.modal.confirm(
        this.intl.t("component.identity-phone-numbers.delete.prompt", options)
      );

      try {
        yield phoneNumber.destroyRecord();
        this.notification.success(
          this.intl.t(
            "component.identity-phone-numbers.delete.success",
            options
          )
        );
      } catch (error) {
        console.error(error);
        this.notification.danger(error.message);
      }
    } catch (error) {
      // Dialog was dimissed. No action necessary.
    }
  }
}
