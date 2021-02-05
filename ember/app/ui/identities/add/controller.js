import Controller from "@ember/controller";
import { action } from "@ember/object";

export default class IdentitiesAddController extends Controller {
  @action onSave(identity) {
    this.transitionToRoute("identities.edit", identity.id);
  }
}
