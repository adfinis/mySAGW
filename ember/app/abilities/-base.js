import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class BaseAbility extends Ability {
  @service session;

  get userGroups() {
    return this.session.data?.authenticated?.userinfo?.mysagw_groups || [];
  }

  get isAdmin() {
    if (!this.session.isAuthenticated) {
      return false;
    }

    return this.userGroups.includes("admin");
  }

  get isStaff() {
    if (!this.session.isAuthenticated) {
      return false;
    }

    return this.userGroups.includes("sagw");
  }

  isOwnIdentity(identity) {
    if (!this.session.isAuthenticated) {
      return false;
    }

    return identity.idpId === this.session.data.authenticated.userinfo.sub;
  }

  isStaffOrOwnIdentity(identity) {
    return this.isStaff || this.isOwnIdentity(identity);
  }

  isInvited(document) {
    return !!document.invitations.findBy(
      "email",
      this.session.data.authenticated.userinfo.email
    );
  }
}
