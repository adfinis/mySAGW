import { validatePresence } from "ember-changeset-validations/validators";

// TODO Validate phone-number format.
//      The pattern included with changeset-validations too strict.
//      validateFormat({ type: "phone" })

export default {
  phone: [validatePresence(true)],
};
