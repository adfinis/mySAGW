import {
  validatePresence,
  validateFormat,
} from "ember-changeset-validations/validators";

export default {
  email: [validatePresence(true), validateFormat({ type: "email" })],
};
