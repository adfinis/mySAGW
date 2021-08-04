import Controller from "@ember/controller";
import { Changeset } from "ember-changeset";
import lookupValidator from "ember-changeset-validations";

import SnippetValidations from "mysagw/validations/snippet";

export default class SnippetsEditController extends Controller {
  get changeset() {
    return Changeset(
      this.model,
      lookupValidator(SnippetValidations),
      SnippetValidations
    );
  }
}
