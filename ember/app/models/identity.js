import Model, { attr, hasMany } from "@ember-data/model";

export default class IdentityModel extends Model {
  @attr idpId;
  @attr organisationName;
  @attr firstName;
  @attr lastName;
  @hasMany("interest") interests;
  @attr isOrganisation;

  fullName() {
    return [this.firstName, this.lastName].filter(Boolean).join(" ");
  }
}
