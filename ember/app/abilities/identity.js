import { readOnly } from "@ember/object/computed";
import BaseAbility from "mysagw/abilities/-base";

export default class IdentityAbility extends BaseAbility {
  @readOnly("isStaff") canList;
  @readOnly("isStaff") canAdd;
  @readOnly("isStaff") canEditOrganisation;
  @readOnly("isStaff") canAddInterest;
  @readOnly("isStaff") canRemoveInterest;

  canEdit(identity) {
    return this.isStaff || this.isAuthenticatedIdentity(identity);
  }
}
