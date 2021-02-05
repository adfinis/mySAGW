import { attr, hasMany } from "@ember-data/model";
import { LocalizedModel } from "ember-localized-model";

export default class IdentityModel extends LocalizedModel {
  @attr idpId;
  @attr organisationName;
  @attr firstName;
  @attr lastName;
  @hasMany emails;
  @hasMany phoneNumbers;
  @hasMany interests;
  @attr isOrganisation;

  get fullName() {
    return [this.firstName, this.lastName].filter(Boolean).join(" ");
  }
}
