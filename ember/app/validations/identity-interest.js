import { validatePresence } from "ember-changeset-validations/validators";

export default {
  interest: [validatePresence(true)],
};
