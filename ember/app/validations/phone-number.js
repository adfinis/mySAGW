import { validatePresence } from "ember-changeset-validations/validators";

// TODO Validate phone-number format.
//      The pattern included with changeset-validations too strict.
//      See validate-format-phone.png for a view of the regex used.
//      validateFormat({ type: "phone" })

export default {
  phone: [validatePresence(true)],
};
