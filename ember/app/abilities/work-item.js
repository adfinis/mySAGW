import { inject as service } from "@ember/service";

import BaseAbility from "mysagw/abilities/-base";
export default class WorkItemAbility extends BaseAbility {
  @service store;

  get canList() {
    const identity = this.store
      .peekAll("identity")
      .findBy("idpId", this.session.data.authenticated.userinfo?.sub);

    const nwpIdentity = identity?.memberships.find(
      (membership) =>
        membership.organisation.get("organisationName")===
          ENV.APP.nwpOrganisationName && !membership.isInactive
    );

    return this.isStaffOrAdmin || Boolean(nwpIdentity);
  }

  get canEdit() {
    return this.isStaffOrAdmin;
  }

  get canShowAll() {
    return this.isStaffOrAdmin;
  }
}
