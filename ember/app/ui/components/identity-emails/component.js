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
import EmailValidations from "mysagw/validations/email";
import UIkit from "uikit";

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
      console.error(error);
      this.notification.danger(error.message);
    }
  }

  // Delete

  @dropTask *delete(email) {
    try {
      const options = { address: email.email };
      yield UIkit.modal.confirm(
        this.intl.t("component.identity-emails.delete.prompt", options)
      );

      try {
        yield email.destroyRecord();
        this.notification.success(
          this.intl.t("component.identity-emails.delete.success", options)
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
