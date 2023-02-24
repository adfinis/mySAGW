import { validatePresence } from "ember-changeset-validations/validators";

export default {
  _title: {
    de: [validatePresence(true)],
  },
};
