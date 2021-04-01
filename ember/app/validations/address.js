import { validatePresence } from "ember-changeset-validations/validators";

export default {
  streetAndNumber: [validatePresence(true)],
};
