import {
  validatePresence,
  validateFormat,
} from "ember-changeset-validations/validators";

export default {
  firstName: [validatePresence(true)],
  lastName: [validatePresence(true)],
  email: [validateFormat({ type: "email" })],
  organisationName: [
    validatePresence({ presence: true, on: "isOrganisation" }),
  ],
};
