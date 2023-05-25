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

    return identity.idpId === this.session.data.authenticated.userinfo.sub;
  }

  isStaffOrOwnIdentity(identity) {
    return this.isStaff || this.isOwnIdentity(identity);
  }

  hasAccess(calumaCase) {
    return (
      this.hasCaseAccess(calumaCase) || this.hasCirculationAccess(calumaCase)
    );
  }

  hasCaseAccess(calumaCase) {
    return Boolean(
      calumaCase.accesses.findBy(
        "identity.idpId",
        this.session.data.authenticated.userinfo.sub
      )
    );
  }

  hasCirculationAccess(calumaCase) {
    return Boolean(
      calumaCase.workItems
        .findBy("task.slug", "circulation")
        ?.childCase.workItems.edges.find(
          (workItem) =>
            workItem.node.task.slug === "circulation-decision" &&
            workItem.node.assignedUsers.includes(
              this.session.data.authenticated.userinfo.sub
            )
        )
    );
  }
}
