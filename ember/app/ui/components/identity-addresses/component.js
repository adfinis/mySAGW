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
import PhoneValidations from "mysagw/validations/address";

/**
 * @arg identity
 */
export default class IdentityAddressesComponent extends Component {
  @service notification;
  @service store;
  @service intl;
  @service fetch;

  // Lifecycle

  @action
  onUpdate() {
    this.fetchCountries.perform();
    this.fetchAddresses.perform(this.args.identity);
  }

  // List

  @lastValue("fetchAddresses") addresses;
  @restartableTask
  *fetchAddresses(identity) {
    return yield this.store.query("address", {
      filter: { identity: identity.id },
    });
  }

  @lastValue("fetchCountries") countries;
  @restartableTask
  *fetchCountries() {
    const adapter = this.store.adapterFor("identity");
    const response = yield this.fetch.fetch(adapter.buildURL("address"), {
      method: "OPTIONS",
      headers: adapter.headers,
    });

    if (response.ok) {
      const data = yield response.json();
      return data.data.actions.POST.country.choices;
    }

    return [];
  }

  // Add / Edit

  validations = PhoneValidations;

  @tracked changeset = null;

  @action edit(address) {
    this.changeset = Changeset(
      address ||
        this.store.createRecord("address", {
          identity: this.args.identity,
        }),
      lookupValidator(PhoneValidations),
      PhoneValidations
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
      // TODO Update `addresses` via Ember Data store.
      this.onUpdate();
      this.changeset = null;
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
      applyError(changeset, error);
    }
  }

  // Delete

  @dropTask
  *delete(address) {
    try {
      const options = { address: address.label };
      yield UIkit.modal.confirm(
        this.intl.t("components.identity-addresses.delete.prompt", options)
      );

      try {
        yield address.destroyRecord();
        this.notification.success(
          this.intl.t("components.identity-addresses.delete.success", options)
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
