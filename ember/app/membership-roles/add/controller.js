import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";

export default class MembershipRolesAddController extends Controller {
  @service("router") router;
  @action onSave(role) {
    this.router.transitionTo("membership-roles.edit", role.id);
  }
}
