import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";

export default class IdentitiesAddController extends Controller {
  @service("router") router;
  @action onSave(identity) {
    this.router.transitionTo("identities.edit", identity.id);
  }
}
