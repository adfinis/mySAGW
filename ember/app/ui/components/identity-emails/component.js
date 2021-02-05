import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
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
    return yield this.store.query("email", {
      filter: { identity: identity.id },
      include: "identity",
    });
  }

  // Add / Edit

  validations = EmailValidations;

  @tracked editItem = null;

  @action edit(email) {
    email =
      email ||
      this.store.createRecord("email", {
        identity: this.args.identity,
      });
    this.editItem = email;
  }

  @action cancel() {
    this.editItem = null;
  }

  @dropTask *submit(changeset) {
    try {
      // Apply changes and save.
      changeset.execute();
      yield this.editItem.save({
        adapterOptions: { include: "identity,identity.emails" },
      });
      // Reset form and list.
      // TODO Update `emails` via Ember Data store.
      this.onUpdate();
      this.editItem = null;
    } catch (error) {
      console.error(error);
      this.notification.danger("ERROR");
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
        this.notification.danger("ERROR");
      }
    } catch (error) {
      console.error(error);
      // Dialog was dimissed. No action necessary.
    }
  }
}
