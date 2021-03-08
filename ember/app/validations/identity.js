import { validatePresence } from "ember-changeset-validations/validators";

export default {
  firstName: [validatePresence(true)],
  lastName: [validatePresence(true)],
  organisationName: [
    validatePresence({ presence: true, on: "isOrganisation" }),
  ],
};
