import { attr, hasMany } from "@ember-data/model";
import { LocalizedModel } from "ember-localized-model";

import { membershipInactive } from "./membership";

export default class IdentityModel extends LocalizedModel {
  @attr idpId;
  @attr salutation;
  @attr title;
  @attr organisationName;
  @attr firstName;
  @attr lastName;
  @attr email;
  @attr language;
  @attr isOrganisation;
  @attr isExpertAssociation;
  @attr isAdvisoryBoard;
  @attr comment;
  @attr hasMemberships;
  @attr hasMembers;
  @attr isAuthorized;

  @hasMany("additional-email", { inverse: "identity", async: true })
  additionalEmails;
  @hasMany("phone-number", { inverse: "identity", async: true }) phoneNumbers;
  @hasMany("address", { inverse: "identity", async: true }) address;
  @hasMany("interest", { async: true }) interests;

  @hasMany("membership", { inverse: "identity", async: true }) memberships;
  @hasMany("membership", { inverse: "organisation", async: true }) members;

  // special attribute from org-memberships endpoint
  @attr roles;

  get fullName() {
    return [this.lastName, this.firstName].filter(Boolean).join(" ");
  }

  get label() {
    return this.fullName;
  }

  get roleMemberships() {
    return this.roles.map((role) => {
      role.timeSlot = role.time_slot;
      role.inactive = membershipInactive(role);

      // resolve a default if translations are not set
      if (role.role) {
        const nonEmptyValue = Object.values(role.role).find((value) => value);
        Object.keys(role.role).forEach((key) => {
          if (!role.role[key]) {
            role.role[key] = nonEmptyValue;
          }
        });
      }

      return role;
    });
  }
}
