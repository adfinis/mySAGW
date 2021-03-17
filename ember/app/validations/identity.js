import {
  validatePresence,
  validateFormat,
} from "ember-changeset-validations/validators";

export default {
  firstName: [],
  lastName: [],
  email: [validateFormat({ type: "email" })],
  organisationName: [
    validatePresence({ presence: true, on: "isOrganisation" }),
  ],
};
