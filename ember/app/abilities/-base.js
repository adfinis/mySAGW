import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class BaseAbility extends Ability {
  @service session;

  get userGroups() {
    return this.session.data.authenticated.userinfo?.mysagw_groups || [];
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

  isOwnIdentity(idpId) {
    if (!this.session.isAuthenticated) {
      return false;
    }

    return idpId === this.session.data.authenticated.userinfo.sub;
  }

  canEditIdentity(identity) {
    if (this.isStaffOrAdmin) {
      return true;
    } else if (this.model.isOrganisation) {
      return this.model.members.any(
        (member) =>
          member.authorized &&
          !member.isInactive &&
          this.isOwnIdentity(member.identity.get("idpId")),
      );
    }

    return this.isOwnIdentity(identity.idpId);
  }

  hasAccess(calumaCase) {
    return Boolean(
      calumaCase.accesses.findBy(
        "identity.idpId",
        this.session.data.authenticated.userinfo.sub,
      ),
    );
  }
}
