import { readOnly } from "@ember/object/computed";
import BaseAbility from "mysagw/abilities/-base";

export default class AdditionalEmailAbility extends BaseAbility {
  @readOnly("isStaff") showMultiLangDescription;

  canAdd(identity) {
    return this.isStaffOrOwnIdentity(identity);
  }

  canEdit(identity) {
    return this.isStaffOrOwnIdentity(identity);
  }

  canDelete(identity) {
    return this.isStaffOrOwnIdentity(identity);
  }
}
