import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";

export default class InterestsAddController extends Controller {
  @service router;

  @action onSave(interest) {
    this.router.transitionTo("interests.edit", interest.id);
  }
}
