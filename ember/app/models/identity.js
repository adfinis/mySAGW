import { attr, hasMany } from "@ember-data/model";
import { LocalizedModel } from "ember-localized-model";

export default class IdentityModel extends LocalizedModel {
  @attr idpId;
  @attr organisationName;
  @attr firstName;
  @attr lastName;
  @attr email;
  @hasMany additionalEmails;
  @hasMany phoneNumbers;
  @hasMany interests;
  @attr isOrganisation;
  @attr hasMemberships;
  @attr hasMembers;

  get fullName() {
    return [this.firstName, this.lastName].filter(Boolean).join(" ");
  }
}
