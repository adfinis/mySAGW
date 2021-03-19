import Controller from "@ember/controller";
import { action } from "@ember/object";

export default class MembershipRolesAddController extends Controller {
  @action onSave(role) {
    this.transitionToRoute("membership-roles.edit", role.id);
  }
}
