import { inject as service } from "@ember/service";

import BaseAbility from "mysagw/abilities/-base";
import ENV from "mysagw/config/environment";

export default class WorkItemAbility extends BaseAbility {
  @service store;

  get canList() {
    const identity = this.store
      .peekAll("identity")
      .findBy("idpId", this.session.data.authenticated.userinfo?.sub);

    const nwpIdentity = identity?.memberships.find(
      (membership) =>
        ENV.APP.circulationOrganisations.includes(
          membership.organisation.get("organisationName")
        ) && !membership.isInactive
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
