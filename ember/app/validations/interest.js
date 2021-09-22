import { validatePresence } from "ember-changeset-validations/validators";

export default {
  titleObject: {
    de: [validatePresence(true)],
  },
};
