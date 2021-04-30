import Controller from "@ember/controller";
import { action } from "@ember/object";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import SnippetValidations from "mysagw/validations/snippet";

export default class SnippetsAddController extends Controller {
  get changeset() {
    return Changeset(
      this.model,
      lookupValidator(SnippetValidations),
      SnippetValidations
    );
  }

  @action
  onSave() {
    this.transitionToRoute("snippets");
  }
}
