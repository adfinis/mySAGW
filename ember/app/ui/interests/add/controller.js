import Controller from "@ember/controller";
import { action } from "@ember/object";

export default class InterestsAddController extends Controller {
  @action onSave(interest) {
    this.transitionToRoute("interests.edit", interest.id);
  }
}
