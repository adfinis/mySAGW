import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";

import SnippetValidations from "mysagw/validations/snippet";

export default class SnippetsAddController extends Controller {
  @service("router") router;
  get changeset() {
    return Changeset(
      this.model,
      lookupValidator(SnippetValidations),
      SnippetValidations,
    );
  }

  @action
  onSave() {
    this.router.transitionTo("snippets");
  }
}
