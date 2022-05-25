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

  get isStaffOrAdmin() {
    return this.isStaff || this.isAdmin;
  }

  isOwnIdentity(identity) {
    if (!this.session.isAuthenticated) {
      return false;
    }

    return (
      identity.get("idpId") === this.session.data.authenticated.userinfo.sub
    );
  }

  isStaffOrOwnIdentity(identity) {
    if (identity) {
      return this.isStaff || this.isOwnIdentity(identity);
    }

    return false;
  }

  hasAccess(document) {
    return Boolean(
      document.accesses.findBy(
        "identity.idpId",
        this.session.data.authenticated.userinfo.sub
      )
    );
  }
}
