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
import EmailValidations from "mysagw/validations/additional-email";

export default class IdentityEmailsComponent extends Component {
  @service notification;
  @service store;
  @service intl;

  // Lifecycle

  @action onUpdate() {
    this.fetchEmails.perform(this.args.identity);
  }

  // List

  @lastValue("fetchEmails") emails;

  @restartableTask *fetchEmails(identity) {
    return yield this.store.query("additional-email", {
      filter: { identity: identity.id },
      include: "identity",
    });
  }

  // Add / Edit

  @tracked changeset = null;

  @action edit(email) {
    this.changeset = Changeset(
      email ||
        this.store.createRecord("additional-email", {
          identity: this.args.identity,
        }),
      lookupValidator(EmailValidations),
      EmailValidations
    );
  }

  @action cancel() {
    this.changeset = null;
  }

  @dropTask *submit(changeset) {
    try {
      // Apply changes and save.
      yield changeset.save({
        adapterOptions: { include: "identity,identity.additional-emails" },
      });

      // Reset form and list.
      // TODO Update `emails` via Ember Data store.
      this.onUpdate();
      this.changeset = null;
    } catch (error) {
      // A "unique" error can only apply to the email address.
      // But as the backend validation doesn't stem from the field itself
      // it cannot automatically be attributed by `applyError`. That's why we add
      // the specific field error manually to the changeset if present.
      const unique = error.errors?.find(({ code }) => code === "unique");
      if (unique) {
        changeset.addError("email", unique.detail);
      }

      console.error(error);
      this.notification.fromError(error);
      applyError(changeset, error);
    }
  }

  // Delete

  @dropTask *delete(email) {
    try {
      const options = { address: email.email };
      yield UIkit.modal.confirm(
        this.intl.t("components.identity-emails.delete.prompt", options)
      );

      try {
        yield email.destroyRecord();
        this.notification.success(
          this.intl.t("components.identity-emails.delete.success", options)
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
