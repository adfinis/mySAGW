import { service } from "@ember/service";

import BaseAbility from "mysagw/abilities/-base";

export default class WorkItemAbility extends BaseAbility {
  @service store;
  @service session;

  get canList() {
    return this.isStaffOrAdmin || this.session.isNwp;
  }

  get canEdit() {
    return this.isStaffOrAdmin;
  }

  get canShowAll() {
    return this.isStaffOrAdmin;
  }
}
