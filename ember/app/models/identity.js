import { attr, hasMany } from "@ember-data/model";
import { LocalizedModel } from "ember-localized-model";

export default class IdentityModel extends LocalizedModel {
  @attr idpId;
  @attr salutation;
  @attr title;
  @attr organisationName;
  @attr firstName;
  @attr lastName;
  @attr email;
  @attr language;
  @hasMany additionalEmails;
  @hasMany phoneNumbers;
  @hasMany("interest") interests;
  @attr isOrganisation;
  @attr isExpertAssociation;
  @attr isAdvisoryBoard;
  @attr comment;
  @attr hasMemberships;
  @attr hasMembers;
  @attr isAuthorized;

  get fullName() {
    return [this.lastName, this.firstName].filter(Boolean).join(" ");
  }

  get label() {
    return this.fullName;
  }
}
